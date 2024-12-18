#!/usr/bin/env python3
import os
import sys
import subprocess

def append_hal(output_hal, output_dir, root_name, internals, tmpdir, sif_path, log_file):
    with open(log_file, 'w') as appendfile:
        for node in internals:
            appendfile.write(f'{node}\n')
            if node == root_name:
                appendfile.write('Node is root node. Nothing to be done.\n')
                appendfile.write('----------\n\n')
                appendfile.flush()
                continue
            
            cmd = [
                'apptainer', 'exec', '--nv', '--cleanenv',
                '--bind', f'{tmpdir}:/tmp', '--bind', f'/scratch:/scratch',
                sif_path, 'halAppendSubtree',
                output_hal, os.path.join(output_dir, f'{node}.hal'),
                node, node, '--merge', '--hdf5InMemory'
            ]
            appendfile.write('RUNNING COMMAND:\n')
            appendfile.write(' '.join(cmd) + '\n')
            appendfile.flush()
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            appendfile.write('COMMAND STDOUT:\n')
            appendfile.write(result.stdout + '\n')
            appendfile.write('COMMAND STDERR:\n')
            appendfile.write(result.stderr + '\n')
            appendfile.write('\nDONE!\n')
            appendfile.write('----------\n\n')
            appendfile.flush()

if __name__ == "__main__":
    output_hal = sys.argv[1]
    output_dir = sys.argv[2]
    root_name = sys.argv[3]
    internals_str = sys.argv[4]
    tmpdir = sys.argv[5]
    sif_path = sys.argv[6]
    log_file = sys.argv[7]
    
    # Convert internals string to dict
    internals = eval(internals_str)
    append_hal(output_hal, output_dir, root_name, internals, tmpdir, sif_path, log_file)