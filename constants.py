THRESHOLDS = list(range(0, 100, 10))
PASS_INDEX = 4
YEARS = list(range(2013, 2018))
SUBJECTS_LONG_TO_SHORT = {
    'advanced classical physics': 'acp',
    # 'advanced electronics': 'ae1',
    'advanced hydrodynamics': 'advhydro',
    'advanced particle physics': 'app',
    'astrophysics': 'astro',
    'atmospheric physics': 'atm',
    # 'atomic, nuclear and particle physics': 'anp2',
    'bsc projects': 'proj3',
    'complexity and networks': 'c&n',
    'communicating physics': 'commPhysics',
    'comprehensives': 'comps',
    'computational neuroscience': 'cns',
    'computational physics': 'cpp',
    'cosmology': 'cos',
    'nanotechnology in consumer electronics': 'nanotech',
    # 'electricity, magnetism and relativity': 'emr1',
    'electromagnetism and optics': 'emop2',
    'environmental physics': 'env',
    'essay projects': 'essay3',
    'foundations of quantum mechanics': 'fqm',
    'general relativity': 'gr',
    'group theory': 'gt',
    'instrumentation': 'inst',
    'information theory': 'it',
    'imaging and biophotonics': 'i&b',
    # 'laboratory & computing 1': 'lc1',
    # 'laboratory & computing 2': 'lc2',
    'laboratory 3': 'lab3',
    'lasers': 'lasers',
    'laser technology': 'lt',
    'light and matter': 'lm',
    'mathematical methods': 'mm',
    'mathematics': 'm1',
    'maths analysis': 'ma1',
    'maths and statistics of measurement': 'msm2',
    'mechanics, vibrations and waves': 'mvw1',
    'medical imaging x-rays & ultrasounds': 'mixu',
    'medical imaging nuclear diagnostics & mri': 'mind',
    'msci projects': 'proj4',
    'optical communications': 'oc',
    'physics of the universe and fluid dynamics': 'pufd',
    'plasma physics': 'plp',
    'plasmonics and metamaterials': 'pm',
    # 'professional skills & basic electronics 1': 'psk1',
    # 'professional skills 2': 'psk2',
    'professional skills 3': 'psk3',
    'quantum field theory': 'qft',
    'quantum information': 'qi',
    # 'quantum mechanics': 'qm2',
    'quantum optics': 'qo',
    # 'quantum physics and structure of matter': 'qpsm1',
    'quantum theory of matter': 'qtm',
    # 'research interfaces': 'ri',
    # 'solid state physics': 'ss2',
    'space physics': 'sp',
    'statistical mechanics': 'sm',
    'sun, stars & planets': 'ssp',
    'thermodynamics and statistical physics': 'tdsp2',
    'unification': 'uni',
    # 'year 1 project': 'pjt1'
}

SUBJECTS_SHORT_TO_LONG = {v: k for k, v in SUBJECTS_LONG_TO_SHORT.items()}
