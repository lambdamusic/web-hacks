# ===========
# LEGACY UNUSED CODE
# ===========
#
# In order to cope with the lack of a 'publisher' filter, the query was enriched by using DOI stems for Springer Nature. This was fixed on February 11, 2019.
#
# The list below could become handy in other situations.
#

DOI_STEMS = {
    '10.1013':
    'Nature Publishing Group',
    '10.1038':
    'Nature Publishing Group',
    '10.1057':
    'Nature Publishing Group - Macmillan Publishers',
    '10.1251':
    'Springer (Biological Procedures Online)',
    '10.1186':
    'Springer (Biomed Central Ltd.)',
    '10.4076':
    'Springer (Cases Network, Ltd.)',
    '10.1114':
    'Springer (Kluwer Academic Publishers - Biomedical Engineering Society',
    '10.1023':
    'Springer (Kluwer Academic Publishers)',
    '10.5819':
    'Springer - (backfiles)',
    '10.1361':
    'Springer - ASM International',
    '10.1379':
    'Springer - Cell Stress Society International',
    '10.1065':
    'Springer - Ecomed Publishers',
    '10.1381':
    'Springer - FD Communications',
    '10.7603':
    'Springer - Global Science Journals',
    '10.1385':
    'Springer - Humana Press',
    '10.4098':
    'Springer - Mammal Research Institute',
    '10.3758':
    'Springer - Psychonomic Society',
    '10.1617':
    'Springer - RILEM Publishing',
    '10.5052':
    'Springer - Real Academia de Ciencias Exactas, Fisicas y Naturales',
    '10.1245':
    'Springer - Society of Surgical Oncology',
    '10.4333':
    'Springer - The Korean Society of Pharmaceutical Sciences and Technology',
    '10.1365':
    'Springer Fachmedien Wiesbaden GmbH',
    '10.1891':
    'Springer Publishing Company',
    '10.1140':
    'Springer-Verlag',
    '10.1007':
    'Springer-Verlag',
}

RESTRICT_CLAUSE = "AND (%s) " % " OR ".join(["doi:%s*" % x for x in DOI_STEMS])
# => AND (doi:10.1038* OR doi:10.1007* OR doi:10.1186*)
