#!/usr/bin/env python
"""Create a BEM model for a subject.

Examples
--------
.. code-block:: console

    $ mne setup_forward_model -s 'sample'

"""

import sys
import os
import mne
from mne.utils import get_subjects_dir


def run():
    """Run command."""
    from mne.commands.utils import get_optparser, _add_verbose_flag

    parser = get_optparser(__file__)

    parser.add_option("-s", "--subject",
                      dest="subject",
                      help="Subject name (required)",
                      default=None)
    parser.add_option("--model",
                      dest="model",
                      help="Output file name. Use a name <dir>/<name>-bem.fif",
                      default=None,
                      type='string')
    parser.add_option('--ico',
                      dest='ico',
                      help='The surface ico downsampling to use, e.g. '
                           ' 5=20484, 4=5120, 3=1280. If None, no subsampling'
                           ' is applied.',
                      default=None,
                      type='int')
    parser.add_option('--brainc',
                      dest='brainc',
                      help='Defines the brain compartment conductivity. '
                           'The default value is 0.3 S/m.',
                      default=0.3,
                      type='float')
    parser.add_option('--skullc',
                      dest='skullc',
                      help='Defines the skull compartment conductivity. '
                           'The default value is 0.006 S/m.',
                      default=0.006,
                      type='float')
    parser.add_option('--scalpc',
                      dest='scalpc',
                      help='Defines the scalp compartment conductivity. '
                           'The default value is 0.3 S/m.',
                      default=0.3,
                      type='float')
    parser.add_option('--homog',
                      dest='homog',
                      help='Use a single compartment model (brain only) '
                           'instead a three layer one (scalp, skull, and '
                           ' brain). If this flag is specified, the options '
                           '--brainc, --skullc, and --scalpc are irrelevant.',
                      default=None,
                      type='float')
    parser.add_option('-d', '--subjects-dir',
                      dest='subjects_dir',
                      help='Subjects directory',
                      default=None)
    _add_verbose_flag(parser)
    options, args = parser.parse_args()

    if options.subject is None:
        parser.print_help()
        sys.exit(1)

    subject = options.subject
    fname = options.model
    subjects_dir = options.subjects_dir
    ico = options.ico
    brainc = options.brainc
    skullc = options.skullc
    scalpc = options.scalpc
    homog = options.homog
    verbose = True if options.verbose is not None else False

    # Parse conductivity option
    if homog is not None:
        # Single layer
        conductivity = [homog]
    else:
        conductivity = [brainc, skullc, scalpc]
    # Create source space
    bem_model = mne.make_bem_model(subject,
                                   ico=ico,
                                   conductivity=conductivity,
                                   subjects_dir=subjects_dir,
                                   verbose=verbose)
    # Generate filename
    if fname is None:
        n_faces = list(str(len(surface['tris'])) for surface in bem_model)
        fname = subject + '-' + '-'.join(n_faces) + '-bem.fif'
    else:
        if not (fname.endswith('-bem.fif') or fname.endswith('_bem.fif')):
            fname = fname + "-bem.fif"
    subjects_dir = get_subjects_dir(subjects_dir, raise_error=True)
    fname = os.path.join(subjects_dir, subject, "bem", fname)
    # Save source space to file
    mne.write_bem_surfaces(fname, bem_model)


mne.utils.run_command_if_main()
