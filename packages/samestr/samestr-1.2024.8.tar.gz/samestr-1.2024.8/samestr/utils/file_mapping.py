import os
from os.path import dirname, abspath, exists
from samestr.utils import ooSubprocess
from samestr.utils.utilities import list_str_all_endswith

import logging
LOG = logging.getLogger(__name__)


def set_output_structure(args):
    """Sets predefined output filenames.

    Additionally creates predefined output dirs if they don't exist.
    """

    # dest
    out_dir =os.path.join(abspath(args[0]['output_dir']), '')
    cmd = args[0]['command']

    ooSubprocess.makedirs(out_dir)

    if cmd == 'convert':

        for arg in args:
            n = arg['bname']

            # metaphlan
            arg['sam'] =os.path.join(arg['input_dir'], n + '.sam.bz2')
            arg['bowtie2out'] =os.path.join(arg['input_dir'], n + '.bowtie2out')
            
            # motus
            arg['bam'] =os.path.join(arg['input_dir'], n + '.bam')

            # taxonomic profiles
            if not arg['tax_profiles_dir']:
                arg['tax_profiles_dir'] = arg['input_dir']
            else:
                arg['tax_profiles_dir'] =os.path.join(abspath(arg['tax_profiles_dir']), '')

            # file name
            arg['tax_profile'] =os.path.join(arg['tax_profiles_dir'], n + arg[
                'tax_profiles_extension'])

            # exists
            if not exists(arg['tax_profile']):
                LOG.error('Taxonomic profile not found: %s' % arg['tax_profile'])
                exit(1)

            # output
            sample_dir =os.path.join(out_dir, n, '')

            ## sam2bam
            arg['sorted_bam'] =os.path.join(sample_dir, n + '.bam')

            ## bam2freq
            arg['gene_file'] =os.path.join(sample_dir, n + '.gene_file.txt.gz')
            arg['contig_map'] =os.path.join(sample_dir, n + '.contig_map.txt.gz')
            arg['kp'] =os.path.join(sample_dir, n + '.kp.txt')
            arg['np'] = sample_dir

            # make sample dirs
            ooSubprocess.makedirs(sample_dir)

    return args


def spread_args_by_input_files(args):
    # spread args to list of args per sample/sample-pair
    spread_args = []
    for idx, (base_name,
              input_files) in enumerate(args['input_files'].items()):

        spread_args.append({})
        for arg in args:
            if not arg == 'input_files':
                spread_args[idx][arg] = args[arg]

        group_size = len(input_files)
        spread_args[idx]['bname'] = base_name
        spread_args[idx]['input_dir'] =os.path.join(dirname(abspath(input_files[0])), '')

        # for paired-end: sanity check for pair counts of two
        if args['input_sequence_type'] == 'paired':
            if group_size > 2:
                LOG.error('More than two samples (%s) found: %s [%s]' %
                          (group_size, base_name, ','.join(input_files)))
                exit(1)
            elif group_size < 2:
                LOG.error('Not all samples are paired: %s.'
                          'Check file extension after read index [%s]' %
                          (base_name, ','.join(input_files)))
                exit(1)
            else:
                spread_args[idx]['1%s' % args['input_extension']] = [
                    f for f in input_files if '1.fastq' in f
                ][0]
                spread_args[idx]['2%s' % args['input_extension']] = [
                    f for f in input_files if '2.fastq' in f
                ][0]

        # for single-end: sanity check 1 observation per base name
        else:
            if group_size > 1:
                LOG.error('More than one sample (%s) found: %s [%s]' %
                          (group_size, base_name, ','.join(input_files)))
                exit(1)
            else:
                spread_args[idx]['%s' %
                                 args['input_extension']] = input_files[0]

    return spread_args


def get_accepted_extension(file, accepted_extensions):
    e = '.' + '.'.join(file.rsplit('.', 1)[-1:])
    if e in accepted_extensions:
        return e
    else:
        e = '.' + '.'.join(file.rsplit('.', 2)[-2:])
        if e in accepted_extensions:
            return e
    return None


def get_uniform_extension(files, accepted_extensions):
    input_extension = get_accepted_extension(files[0], accepted_extensions)

    if not input_extension:
        LOG.error('Files must be supplied with accepted file extensions: %s' %
                  ', '.join(accepted_extensions))
        exit(1)

    if not list_str_all_endswith(files, input_extension):
        LOG.error('Not all files have the same file extension.')
        exit(1)

    return input_extension


def clade_path(name, filebase=False):
    # Initialize segments list
    segments = []

    # Define the cut positions
    cuts = [9, 12, 15]

    # Track the previous cut position
    prev_cut = 0

    # Add segments at specified cut positions
    for cut in cuts:
        if len(name) > prev_cut:
            segment = name[prev_cut:cut] if len(name) >= cut else name[prev_cut:]
            segments.append(segment)
            prev_cut = cut
        else:
            break

    # Combine the segments to form the path
    pseudo_path =os.path.join('/db_markers', *segments, '')

    # Add name as file basis
    if filebase:
        pseudo_path += name

    return pseudo_path