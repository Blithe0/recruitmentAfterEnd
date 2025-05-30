# app/resume_parser/schema_map.py
label_list = ['O', 'B-name', 'I-name', 'B-phone', 'I-phone', 'B-email', 'I-email', 'B-school', 'I-school', 'B-skill', 'I-skill']
label_map = {i: label for i, label in enumerate(label_list)}

# label_map = {
#     0: 'O',
#     1: 'B-name',
#     2: 'I-name',
#     3: 'B-gender',
#     4: 'I-gender',
#     5: 'B-age',
#     6: 'I-age',
#     7: 'B-degree',
#     8: 'I-degree',
#     9: 'B-phone',
#     10: 'I-phone',
#     11: 'B-email',
#     12: 'I-email',
#     13: 'B-job_target',
#     14: 'I-job_target',
#     15: 'B-skills',
#     16: 'I-skills'
# }
