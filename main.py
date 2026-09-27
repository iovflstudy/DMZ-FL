"""DMZ-FL single-experiment entry."""
import argparse
import logging
import os
from global_utils import setup_seed, setup_logger


def parse_args():
    p = argparse.ArgumentParser(description='Run a single DMZ-FL experiment.')
    p.add_argument('--config', required=True, help='path to YAML config')
    p.add_argument('--output', default='results/run')
    p.add_argument('--attack', default='none',
                   choices=['none', 'sign_flip', 'gradient_scaling', 'label_flipping'])
    p.add_argument('--malicious_ratio', type=float, default=0.0)
    p.add_argument('--seed', type=int, default=42)
    return p.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)
    logger = setup_logger('dmzfl', args.output)
    setup_seed(args.seed)
    logger.info(f'Config: {args.config} | attack={args.attack} '
                f'malicious={args.malicious_ratio}')
    # TODO(engine): load data -> init clients/server -> run FL loop.
    # Wire up dmzfl.engine.coordinator once the engine module is implemented.
    logger.info('Entry point ready. Engine wiring pending (see dmzfl/engine/).')


if __name__ == '__main__':
    main()