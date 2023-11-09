"""A transparent linear-interpolation resampler, not a band-limited converter."""
import argparse
import json
import math
from pathlib import Path

def resample(samples, input_rate, output_rate):
    for rate in (input_rate, output_rate):
        if isinstance(rate, bool) or not isinstance(rate, int) or rate < 1:
            raise ValueError('Rates must be positive integers')
    if not isinstance(samples, list) or any((isinstance(x, bool) or not isinstance(x, (int, float)) or (not math.isfinite(x)) or (abs(x) > 1) for x in samples)):
        raise ValueError('Samples must be finite normalized numbers')
    if not samples:
        return []
    count = (len(samples) * output_rate + input_rate - 1) // input_rate
    if count > 10000000:
        raise ValueError("Output exceeds the demo's 10-million-sample limit")
    output = []
    for i in range(count):
        position = i * input_rate / output_rate
        left = min(int(position), len(samples) - 1)
        right = min(left + 1, len(samples) - 1)
        fraction = position - left
        output.append(samples[left] * (1 - fraction) + samples[right] * fraction)
    return output

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, help='JSON {samples:[...], input_rate:int, output_rate:int}')
    args = parser.parse_args()
    try:
        p = json.loads(args.input.read_text()) if args.input else {'samples': [0, 0.5, 1, 0.5, 0, -0.5, -1, -0.5], 'input_rate': 8000, 'output_rate': 12000}
        if not isinstance(p, dict):
            raise ValueError('Input must be an object')
        output = resample(p['samples'], p['input_rate'], p['output_rate'])
        print(json.dumps({'input_samples': len(p['samples']), 'output_samples': len(output), 'samples': output, 'limitation': 'No anti-alias filter; use a band-limited DSP library for audio quality'}, indent=2))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.error(str(exc))
if __name__ == '__main__':
    main()
