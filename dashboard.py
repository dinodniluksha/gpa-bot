import re
import scrapper, helper, main
from bs4 import BeautifulSoup
from flask import Flask, session

result_table = {}
string_html = ''

script = '''
            <script>
            const class_types = ["l1s2", "l1s1", "l2s2", "l2s1", "l3s2", "l3s1", "l4s2", "l4s1"];

            function update_sem_gpa(select_box) {
                var grade_value;
                var credit_value;

                console.log("Hitting Drop Down List");
                grade_value = select_box.value;
                var x = select_box.getAttribute('name');
                console.log(x);

                find_sem_gpa(x);
                find_overall_gpa();
            }

            function find_sem_gpa(sem_class){
                rack = document.getElementsByClassName(sem_class);
                console.log(rack[0].childNodes);

                var sgpa = 0.0;
                var sum_mul = 0.0;
                var sum_credit = 0.0;

                for (let i = 0; i < rack.length; i++) {

                    console.log(i)

                    var grade_val = rack[i].childNodes[2].firstChild.value
                    var credit_val = rack[i].childNodes[3].innerHTML;

                    console.log(grade_val);
                    console.log(credit_val);

                    if (credit_val == "-"){
                        sum_mul = sum_mul + grade_val*0.0;
                        console.log(sum_mul);
                        sum_credit = sum_credit + 0.0;
                        console.log(sum_credit);
                    } 
                    else{
                        sum_mul = sum_mul + grade_val*parseFloat(credit_val);
                        console.log(sum_mul);
                        sum_credit = sum_credit + parseFloat(credit_val);
                        console.log(sum_credit);
                    }
                }

                sgpa = sum_mul/sum_credit;
                console.log("hello console");
                console.log("SGPA : " + sgpa.toFixed(2));

                //to do :- catching relevant display section (span) & displaying (primitive SGPA) SGPA or hide (NAN SGPA)
                if(sum_mul==0 && sum_credit==0){
                    document.getElementById(sem_class).innerHTML = "";
                }
                else{
                    document.getElementById(sem_class).innerHTML = "SGPA : " + sgpa.toFixed(2);
                }
            }

            window.onload = function find_overall_sgpa(){
                console.log("Triggering onload function");

                for(let i = 0; i < class_types.length; i++){
                    find_sem_gpa(class_types[i]);
                }

                find_overall_gpa();
            };

            function find_overall_gpa(){
                console.log("Calculating Updated OGPA");

                var ogpa = 0.0;
                var sum_sgpa = 0.0
                var sem_count = 0

                for(let i = 0; i < class_types.length; i++){
                    var sgpa = document.getElementById(class_types[i]).innerHTML;
                    //console.log(sgpa);

                    if(sgpa != ""){
                        const regex = /\d.\d\d/g;
                        const found = sgpa.match(regex);
                        console.log(parseFloat(found[0]));

                        sum_sgpa = sum_sgpa + parseFloat(found[0]);
                        sem_count++;
                    }  
                }
                ogpa = sum_sgpa/sem_count;
                console.log(ogpa.toFixed(2));

                document.getElementById("ogpa").innerHTML = ogpa.toFixed(2);
            }           

            function reset_result(){
                console.log("Hitting Rest Button");
                window.location.reload();
            }

            function logout(){
                console.log("Clicking Logout Button");

                window.open("http://127.0.0.1:5000/logout", "_self");
            }
            </script>
         '''


def is_table_content(row):
    output = re.findall("<tr class=\"bodytext\">", row)
    # print(output)
    if output:
        return True
    else:
        return False


def func(key):
    table_head = ''
    global string_html
    row_table = [
        '<div style="position:fixed;top:20px;right:20px;height:80px;width:200px;background-color: rgb(242, 255, 59);padding:10px;display:flex;justify-content:center;flex-direction:column;"><div>',
        '<table class="bodytextbold"><tbody><tr><td><b>Overall GPA</b></td><td><b>:</b></td><td><b><span id="ogpa">0</span></b></td></tr></tbody></table></div>'
        '<button onclick="reset_result()" style="border:none;border-radius:10px;margin:10px 20px 5px 20px;color:white;padding:10px 25px;font-size:16px;font-weight:550;cursor:pointer;background-color:#008CBA;">RESET</button></div>',
        '<button onclick="logout()" style="border:none;border-radius:10px;margin:10px 20px 5px 20px;color:white;padding:10px 25px;font-size:16px;font-weight:550;cursor:pointer;background-color:#008CBA;"> LOGOUT</button>',
        '<table background="images\water_mark.png" border="1" cellpadding="2" class="Text_table"><tbody>'
    ]

    result_list = re.findall("<tr.*</tr>", str(scrapper.result_table[0]))
    print(len(result_list), " : ", result_list)

    level_digit = 0
    sem_digit = 0

    for item in result_list:
        if is_table_content(item):
            tracking_class = f'l{level_digit}s{sem_digit}'

            x = re.search("<td>[A-Z]{2}[0-9]{4}</td>", item)
            module_code = x.group()

            if level_digit != 0 and sem_digit != 0:
                item = re.sub('<tr class="bodytext">', f'<tr class="bodytext {tracking_class}">', item)
                onchange_function = True
            else:
                onchange_function = False

            z = re.search('font class="bodytext.*</font', item)
            grade_part = z.group()
            print(grade_part)
            decode = re.split(r"[<>]", grade_part)
            print(decode[1])
            print(f'bodytext {tracking_class}', decode[1], onchange_function)
            add_item = helper.build_option_menu(tracking_class, onchange_function, decode[1])

            item = re.sub(f'<font class="bodytext.*>{decode[1]}[+]*</font>', add_item, item)

            mod_item = re.sub("<tr><td.*> SGPA : NOT APPLICABLE</font></strong><br/><br/></td></tr>", "", item)

            if onchange_function:
                mod_item = re.sub('<strong><font .*SGPA : .*</font></strong>',
                                  f'<span id={tracking_class} style="color:blue; font-weight: 900;">SGPA : 0</span>',
                                  mod_item)
                mod_item = re.sub('<b>SGPA : .*</b>',
                                  f'<span id={tracking_class} style="color:blue; font-weight: 900;">SGPA : 0</span>',
                                  mod_item)
            else:
                mod_item = re.sub('<strong><font .*SGPA : .*</font></strong>', '', mod_item)
                mod_item = re.sub('<b>SGPA : .*</b>', '', mod_item)

            print(mod_item)

            result_table[table_head][module_code] = mod_item
        else:
            y = re.findall("Level [0-9][,a-zA-Z\s]*[0-9]+", item)
            # stage = y.group()

            if y:
                print(y[0], '------------------------------')
                digits = re.findall("[0-9]", y[0])
                level_digit = digits[0]
                sem_digit = digits[1]
            else:
                # print('Not Consider------------------------------')
                level_digit = 0
                sem_digit = 0

            table_head = re.sub("[0-9]{4} / [0-9]{4} - ", "", item)

            if not table_head in result_table.keys():
                result_table[table_head] = {}

    print(result_table)
    for t_head in result_table:
        # print(t_head)
        row_table.append(t_head)
        for t_content in result_table[t_head]:
            # print(result_table[t_head][t_content])
            # print("Module")
            row_table.append(result_table[t_head][t_content])

    # removing unnecessary segments
    row_table.append('</tbody></table>')
    row_table.append(script)
    # print(row_table)

    string_html = '\n'.join(row_table)
    print(string_html)
