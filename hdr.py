#!/usr/bin/env python

import os
import sys
import logging
import platform
import argparse
from app.logger import log
import app.pipeline


def load_prompts(prompts_file):
    with open(prompts_file, 'r', encoding='utf8') as f:
        return [line.strip() for line in f.readlines()]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HDR')
    parser.add_argument('--dtype', type=str, default='bfloat16', help='torch dtype')
    parser.add_argument('--device', type=str, default='cuda:0', help='torch device')
    parser.add_argument('--model', type=str, required=True, help='sd model')
    parser.add_argument('--width', type=int, default=1024, help='image width')
    parser.add_argument('--height', type=int, default=1024, help='image height')
    parser.add_argument('--steps', type=int, default=20, help='sampling steps')
    parser.add_argument('--seed', type=int, default=-1, help='noise seed')
    parser.add_argument('--cfg', type=float, default=7.0, help='cfg scale')
    parser.add_argument('--sampler', type=str, default='UniPCMultistepScheduler', help='sd sampler')
    parser.add_argument('--prompts', type=str, required=True, help='prompts file')
    parser.add_argument('--output', type=str, required=True, help='output folder')
    parser.add_argument('--exp', type=float, default=1.0, help='exposure correction')
    parser.add_argument('--timestep', type=int, default=200, help='correction timestep')
    parser.add_argument('--save', action='store_true', help='save interim images')
    parser.add_argument('--hdr', action='store_true', help='create 16bpc hdr image')
    parser.add_argument('--ldr', action='store_true', help='create 8bpc hdr image')
    parser.add_argument('--json', action='store_true', help='save params to json')
    parser.add_argument('--debug', action='store_true', help='debug log')
    args = parser.parse_args()
    if args.debug:
        log.setLevel(logging.debug)
    log.info('HDR start')
    log.info(f'Env: python={platform.python_version()} platform={platform.system()} bin="{sys.executable}" venv="{sys.prefix}"')
    log.info(f'Args: {args}')

    prompts = load_prompts(args.prompts)
    os.makedirs(args.output, exist_ok=True)
    app.pipeline.load(args)
    for i, prompt in enumerate(prompts):
        if len(prompt) == 0:
            continue
        log.info(f'Sequence: count={i+1}/{len(prompts)}')
        app.pipeline.run(args, prompt)
    log.info('HDR end')
