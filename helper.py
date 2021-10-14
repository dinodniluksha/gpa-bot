import re


def build_option_menu(element_name, update_effect, grade):
    options = []
    if update_effect:
        start_text = f'<select name="{element_name}" onchange="update_sem_gpa(this)">'
    else:
        start_text = '<select>'

    option_rack = {'start': f'{start_text}',
                   'Pending': '<option value=0>Pending</option>',
                   'A+': '<option value=4.2>A+</option>',
                   'A': '<option value=4.0>A</option>',
                   'A-': '<option value=3.7>A-</option>',
                   'B+': '<option value=3.3>B+</option>',
                   'B': '<option value=3.0>B</option>',
                   'B-': '<option value=2.7>B-</option>',
                   'C+': '<option value=2.3>C+</option>',
                   'C': '<option value=2.0>C</option>',
                   'C-': '<option value=1.5>C-</option>',
                   'D': '<option value=1.0>D</option>',
                   'I': '<option value=0.0>I</option>',
                   'end': '</select>'
                   }

    # print(option_rack[grade])
    option_rack[grade] = re.sub(f'>{grade}[+]*', f' selected>{grade}', option_rack[grade])

    for key in option_rack:
        # print(option_rack[key])
        options.append(option_rack[key])

    option_text = ''.join(options)

    option_rack[grade] = re.sub(f' selected>{grade}', f'>{grade}', option_rack[grade])

    # for key in option_rack:
    #     print(option_rack[key])

    return option_text
