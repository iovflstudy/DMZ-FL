// DMZ-FL Bulletproofs range-proof micro-benchmark.
//
// Reproduces the deployed 32-bit range proof over the quantized norm slack
// n = floor((B^2 - ||g||^2) * 2^32 / B^2), i.e. the statement 0 <= n < 2^32
// (equivalently ||g||_2 <= B), and measures:
//   1. the per-proof prove/verify latency and serialized proof size (m = 1);
//   2. the total verification wall-clock time as the number of independent
//      proofs (one per selected vehicle) grows from 1 to 1000.
//
// Each proof is independent, exactly as in deployment. The second part mirrors
// the VFL-Chain verification-time methodology and confirms linear scaling.
//
// Production backend: dalek-cryptography `bulletproofs` v5 over the Ristretto
// group of `curve25519-dalek` v4. No trusted setup.
//
// Run:  cargo run --release

use bulletproofs::{BulletproofGens, PedersenGens, RangeProof};
use curve25519_dalek::scalar::Scalar;
use merlin::Transcript;
use rand::rngs::OsRng;
use rand::Rng;
use std::time::Instant;

const N_BITS: usize = 32;
const TRANSCRIPT: &[u8] = b"DMZFL-norm-slack";

fn prove_one(
    bp: &BulletproofGens,
    pc: &PedersenGens,
    secret: u64,
) -> (RangeProof, curve25519_dalek::ristretto::CompressedRistretto) {
    let blinding = Scalar::random(&mut OsRng);
    RangeProof::prove_single(
        bp,
        pc,
        &mut Transcript::new(TRANSCRIPT),
        secret,
        &blinding,
        N_BITS,
    )
    .expect("prove_single failed")
}

fn verify_one(
    proof: &RangeProof,
    bp: &BulletproofGens,
    pc: &PedersenGens,
    comm: &curve25519_dalek::ristretto::CompressedRistretto,
) {
    proof
        .verify_single(
            bp,
            pc,
            &mut Transcript::new(TRANSCRIPT),
            comm,
            N_BITS,
        )
        .expect("verify_single failed");
}

fn main() {
    let bp = BulletproofGens::new(64, 8);
    let pc = PedersenGens::default();

    // ---- 1. Per-proof baseline (m = 1, one proof per vehicle) ----
    let warm = 20;
    for _ in 0..warm {
        let (p, c) = prove_one(&bp, &pc, rand::thread_rng().gen::<u32>() as u64);
        verify_one(&p, &bp, &pc, &c);
    }
    let reps = 50;
    let mut prove_ms = Vec::new();
    let mut verify_ms = Vec::new();
    let mut proof_bytes = 0usize;
    for _ in 0..reps {
        let v = rand::thread_rng().gen::<u32>() as u64;
        let t0 = Instant::now();
        let (p, c) = prove_one(&bp, &pc, v);
        prove_ms.push(t0.elapsed().as_secs_f64() * 1000.0);
        proof_bytes = p.to_bytes().len();
        let t1 = Instant::now();
        verify_one(&p, &bp, &pc, &c);
        verify_ms.push(t1.elapsed().as_secs_f64() * 1000.0);
    }
    prove_ms.sort_by(|a, b| a.partial_cmp(b).unwrap());
    verify_ms.sort_by(|a, b| a.partial_cmp(b).unwrap());
    println!("=== Per-proof baseline (32-bit range proof, m=1; {} reps) ===", reps);
    println!(
        "prove_ms: best={:.2} median={:.2} | verify_ms: best={:.2} median={:.2} | proof_bytes={}",
        prove_ms[0], prove_ms[reps / 2], verify_ms[0], verify_ms[reps / 2], proof_bytes
    );

    // ---- 2. Batch verification vs number of independent proofs (vehicles) ----
    let ns = [1usize, 10, 50, 70, 100, 200, 500, 1000];
    let max_n = *ns.iter().max().unwrap();
    println!("\nGenerating {} independent proofs (not timed)...", max_n);
    let mut proofs: Vec<(RangeProof, curve25519_dalek::ristretto::CompressedRistretto)> =
        Vec::with_capacity(max_n);
    for _ in 0..max_n {
        proofs.push(prove_one(&bp, &pc, rand::thread_rng().gen::<u32>() as u64));
    }

    let rounds = 15;
    println!("\n=== Total verification time vs number of selected clients ({} rounds) ===", rounds);
    println!("N,total_best_ms,total_median_ms,per_proof_median_ms");
    for &n in ns.iter() {
        let mut t = Vec::new();
        for _ in 0..rounds {
            let t0 = Instant::now();
            for (p, c) in proofs.iter().take(n) {
                verify_one(p, &bp, &pc, c);
            }
            t.push(t0.elapsed().as_secs_f64() * 1000.0);
        }
        t.sort_by(|a, b| a.partial_cmp(b).unwrap());
        let best = t[0];
        let med = t[rounds / 2];
        println!("{},{:.2},{:.2},{:.3}", n, best, med, med / n as f64);
    }
}
