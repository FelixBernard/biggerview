import os

# LaTeX-Dokument als Vorlage
latex_template = r"""
\documentclass{{extarticle}}
\pagenumbering{{gobble}}
\renewcommand\thesection{{\arabic{{section}}}}
\author{{---}}
\title{{Accounting}}
\date{{\today}}

\begin{{document}}
\maketitle
\begin{{center}}
\section{{Tabelle}}
% \begin{{table}}
\begin{{tabular}}{{|c|c|c|}}
\hline   
Name & Alter & Stadt \\
\hline
{name} & {age} & {city} \\
\hline
\end{{tabular}}
\end{{center}}
\end{{document}}
"""


def erstelle_latex_pdf(dateiname, nutzer_daten):
    tex_datei = dateiname + ".tex"

    # LaTeX-Datei mit Nutzerdaten füllen
    with open(tex_datei, "w", encoding="utf-8") as f:
        f.write(latex_template.format(
            name=nutzer_daten["Name"],
            age=nutzer_daten["Alter"],
            city=nutzer_daten["Stadt"]
        ))
    os.system(f'latex  -recorder  "nutzer_info.tex"')
    print(f"PDF '{dateiname}.pdf' wurde erfolgreich erstellt!")

def make_pdf(self, data, name = 'main'):
        with open('../user/user_tmp/pdf_tmp.tex', 'r') as f:
            tmp = f.readlines()
        foo = r'\author'
        tmp[3] = foo + '{'+self.name+'}\n'
        with open('../user/'+self.lower_name+'/pdf/list.tex', 'w') as file:
            file.writelines(tmp)
            for n in data:
                file.writelines(f'{n[0]} & {n[1]} & {n[2]} & {n[3]} & {n[4]} & {n[5]} \\\ \n')
                file.writelines('\hline\n')
                # for m in n:
                #     file.writelines(str(m))
            # file.writelines('\end'+'{'+'tabular}\n')
            # # file.writelines('\end'+'{'+'table}\n')
            # file.writelines('\section'+'{'+'Infos}\n')
            # file.writelines('Here are intersting Inforamtions\n')
            # file.writelines('\end'+'{'+'center}\n')
            # file.writelines('\end'+'{'+'document}')
            endings = r"""
            \end{{tabular}}
            \section{{Infos}}
            Here are intersting Information
            \end{{center}}
            \end{{document}}
            """
            file.writelines(endings)
        print(os.getcwd())
        e = {os.path.abspath('../user/'+self.lower_name+'/pdf')}
        os.chdir(os.path.abspath('../user/'+self.lower_name+'/pdf'))
        print(str(e))
        os.system(f'latex  -recorder  "list.tex"') #{os.path.abspath('..')}
        os.chdir(os.path.abspath('../../'))
        print(os.path, 'ok')
        print(os.path.abspath('..'))