# Draw accuracy & latency curve from the searching log directory "logs"

import argparse
from cProfile import label
from collections import defaultdict
import os
import re
from typing import Dict

import matplotlib.pyplot as plt


class LogData:

    def __init__(self, log_dir: str):
        self.log_dir = log_dir
    
    @property 
    def vaild_console_path(self) -> str:
        return os.path.join(self.log_dir, 'logs', 'valid_console.txt')

    @property
    def vaild_lines(self) -> str:
        try:
            return self._vaild_lines
        except:
            self._vaild_lines = []
            f = open(self.vaild_console_path, 'r')
            line = f.readline()
            while line:
                if line.startswith('Valid'):
                    self._vaild_lines.append(line)
                line = f.readline()
            f.close()
            return self._vaild_lines

    @property
    def vaild_data_dict(self) -> Dict:
        try:
            return self._vaild_data_dict
        except:
            self._vaild_data_dict = defaultdict(lambda: [])
            for line in self.vaild_lines:
                match = re.match(r'.*top-1 acc (\d*\.?\d+).*Latency-mobile: (\d*\.?\d+)ms', line)
                top1_acc, latency_ms = match.groups()
                self._vaild_data_dict['top1_acc'].append(round(float(top1_acc), 1))
                self._vaild_data_dict['latency_ms'].append(round(float(latency_ms), 1))
            print(self.vaild_data_dict)
            return self._vaild_data_dict

    @property
    def output_image_path(self) -> str:
        return os.path.join(self.log_dir, 'logs', 'vaild_acc_latency.png')

    def visualize(self):
        num_epochs = len(self.vaild_data_dict['top1_acc'])
        xs = range(1, num_epochs + 1)
        plt.plot(xs, self.vaild_data_dict['top1_acc'], label='vaildation top-1 accuracy')
        plt.plot(xs, self.vaild_data_dict['latency_ms'], label='latency (ms)')
        plt.xlabel('Epochs')
        plt.legend()
        plt.savefig(self.output_image_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_dir', required=True, help='architecture search log dir')
    args = parser.parse_args()

    log_data = LogData(args.log_dir)
    log_data.visualize()


if __name__ == '__main__':
    main()