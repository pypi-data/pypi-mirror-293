from ..game.game import Game
from ..game.cluster import Cluster
from ..game.quest import Quest
from ..game.task import Task
from ..game.xp import XP
from ..game.graph import Graph
import random
from .opener import Opener
from ..run.basic import Success
from typing import List, Any, Dict, Callable, Tuple
from ..settings.settings import Settings
from ..settings.app_settings import AppSettings
from ..settings.rep_settings import languages_avaliable, RepData
from ..down import Down
from ..util.sentence import Sentence, Token,  RToken
from .fmt import Fmt
from .frame import Frame
from .style import Style
import urllib
from .images import opening, random_get
import datetime

from .floating import Floating
from .floating_manager import FloatingManager
from .flags import Flag, Flags, FlagsMan
from .tasktree import TaskTree
from ..actions import Run
from ..run.param import Param


import webbrowser
import os
import curses

class Actions:
    ler_online = "Github"
    sair = "Sair"
    ajuda = "Ajuda"
    baixar = "Baixar"
    ativar = "Ativar"
    navegar = "←↓→"
    editar = "Editar"
    marcar = "Marcar"
    desmarcar = "Desmarcar"
    colapsar = "Colapsar"
    pesquisar = "Buscar"

class Key:
    left = "a"
    # left2 = "h"
    right = "d"
    # right2 = "l"
    down = "s"
    # down2 = "j"
    up = "w"
    # up2 = "k"

    down_task = "b"
    # select_task = "t"
    select_task = "\n"
    ajuda = "h"
    expand = ">"
    expand2 = "."
    collapse = "<"
    collapse2 = ","
    inc_grade = "+"
    inc_grade2 = "="
    dec_grade = "-"
    dec_grade2 = "_"
    set_root_dir = "D"
    set_lang = "L"
    github_open = "g"
    quit = "q"
    # toggle_space = " "
    # toggle_enter = "\n"
    edit= "e"
    cores = "C"
    bordas = "B"
    pesquisar = "/"

class Play:
    def __init__(
        self,
        app: AppSettings,
        game: Game,
        rep_data: RepData,
        rep_alias: str
    ):
        self.app = app
        self.rep_alias = rep_alias
        self.rep = rep_data
        self.settings = Settings()
        self.exit = False

        if self.rep.get_lang() == "":
            self.rep.set_lang(self.app.get_lang_def())
        self.flagsman = FlagsMan(self.rep.get_flags())
        
        self.game: Game = game
        self.fman = FloatingManager()
        self.tree = TaskTree(app, game, rep_data, rep_alias)

        if len(self.rep.get_tasks()) == 0:
            self.show_help()

        self.first_loop = True
        self.graph_ext = ""

        self.help_basic: List[Sentence] = [
            Sentence() + RToken("Y", f"{Actions.pesquisar}[{Key.pesquisar}]"),
            Sentence() + RToken("Y", f"{Actions.marcar} {Key.inc_grade}{Key.dec_grade}"),
        ]

        self.help_fixed: List[Sentence] = [
            Sentence() + RToken("C", f"  {Actions.sair}[{Key.quit}]"),
            Sentence() + RToken("C", f"{Actions.editar}[{Key.edit}]"),
            Sentence() + RToken("G", f"{Actions.ativar}[↲]"),
        ]
        self.help_others_before: List[Sentence] = [
            Sentence() + RToken("Y", f" {Actions.ajuda}[{Key.ajuda}]"),
            Sentence() + RToken("Y", f"{Actions.ler_online}[{Key.github_open}]"),
        ]
        self.help_others_after: List[Sentence] = [
            Sentence() + RToken("Y", f"{Actions.baixar}[{Key.down_task}]"),
            Sentence() + RToken("Y", f"{Actions.navegar}[wasd]")
        ]

        self.wrap_size = Sentence(" ").join(self.build_bottom_array()).len()
        self.opener = Opener(tree=self.tree, fman=self.fman, geral=app, rep_data=rep_data, rep_alias=rep_alias)

        self.search_mode: bool = False
        self.backup_expanded: List[str] = []
        self.backup_index_selected = 0
        self.backup_admin_mode = False

    def save_to_json(self):
        self.tree.save_on_rep()
        self.rep.set_flags(self.flagsman.get_data())
        self.settings.save_settings()
        self.rep.save_data_to_json()

    def set_rootdir(self, only_if_empty=True):
        if only_if_empty and self.app.get_rootdir() != "":
            return

        def chama(value):
            if value == "yes":
                self.app.set_rootdir(os.path.abspath(os.getcwd()))
                self.save_to_json()
                self.fman.add_input(
                    Floating()
                    .put_text("")
                    .put_text("Diretório raiz definido como ")
                    .put_text("")
                    .put_text("  " + os.getcwd())
                    .put_text("")
                    .put_text("Você pode também pode alterar")
                    .put_text("o diretório raiz navegando para o")
                    .put_text("diretório desejado e executando o comando")
                    .put_text("")
                    .put_text("  tko config --root .")
                    .put_text("")
                    .warning()
                )
            else:
                self.fman.add_input(
                    Floating()
                    .put_text("")
                    .put_text("Navegue para o diretório desejado e tente novamente.")
                    .put_text("")
                    .put_text("Você pode também pode alterar")
                    .put_text("o diretório raiz navegando para o")
                    .put_text("diretório desejado e executando o comando")
                    .put_text("")
                    .put_text("tko config --root .")
                    .put_text("")
                    .warning()
                )

        self.fman.add_input(
            Floating()
            .put_text("")
            .put_text("Você deseja utilizar o diretório")
            .put_text("atual como diretório raiz do tko?")
            .put_text("")
            .put_text(os.getcwd())
            .put_text("")
            .put_text("como raiz para o repositório de " + self.rep_alias + "?")
            .put_text("")
            .put_text("Selecione e tecle Enter")
            .put_text("")
            .set_options(["yes", "no"])
            .answer(chama)
        )

    def set_language(self, only_if_empty=True):
        if only_if_empty and self.rep.get_lang() != "":
            return

        def back(value):
            self.rep.set_lang(value)
            self.save_to_json()
            self.fman.add_input(
                Floating()
                .put_text("")
                .put_text("Linguagem alterada para " + value)
                .put_text("")
                .warning()
            )

        self.fman.add_input(
            Floating()
            .put_text("")
            .put_text("Escolha a extensão default para os rascunhos")
            .put_text("")
            .put_text("Selecione e tecle Enter.")
            .put_text("")
            .set_options(languages_avaliable)
            .answer(back)
        )

    def check_root_and_lang(self):
        if self.app.get_rootdir() == "":
            # self.set_rootdir()
            self.fman.add_input(
                Floating()
                .put_text("")
                .put_text("O diretório de download padrão")
                .put_text("do tko ainda não foi definido.")
                .put_text("")
                .put_sentence(Sentence() + "Utilize o comando " + Token("Shift + " + Key.set_root_dir, "g"))
                .put_text("para configurá-lo.")
                .put_text("")
            )

        if self.rep.get_lang() == "":
            self.fman.add_input(
                Floating()
                .put_text("")
                .put_text("A linguagem de download padrão")
                .put_text("para os rascunhos ainda não foi definda.")
                .put_text("")
                .put_sentence(Sentence() + "Utilize o comando " + Token("Shift + " + Key.set_lang, "g"))
                .put_text("para configurá-la.")
                .put_text("")
            )
            return


    def open_link(self):
        obj = self.tree.get_selected()
        if isinstance(obj, Task):
            task: Task = obj
            if task.link.startswith("http"):
                try:
                    webbrowser.open_new_tab(task.link)
                except Exception as _:
                    pass
            self.fman.add_input(
                Floating("v>")
                .set_header(" Abrindo link ")
                .put_text("\n" + task.link + "\n")
                .warning()
            )
        elif isinstance(obj, Quest):
            self.fman.add_input(
                Floating("v>")
                .put_text("\nEssa é uma missão.")
                .put_text("\nVocê só pode abrir o link")
                .put_text("de tarefas.\n")
                .error()
            )
        else:
            self.fman.add_input(
                Floating("v>")
                .put_text("\nEsse é um grupo.")
                .put_text("\nVocê só pode abrir o link")
                .put_text("de tarefas.\n")
                .error()
            )

    def generate_graph(self):
        if not self.first_loop:
            return
        if self.graph_ext == "":
            return
        reachable: List[str] = self.game.available_quests
        counts = {}
        for q in self.game.quests.values():
            done = len([t for t in q.get_tasks() if t.is_complete()])
            init = len([t for t in q.get_tasks() if t.in_progress()])
            todo = len([t for t in q.get_tasks() if t.not_started()])
            counts[q.key] = f"{done} / {done + init + todo}\n{q.get_percent()}%"

        # mark_opt = Flags.dots.is_true()
        Graph(self.game).set_opt(False).set_reachable(reachable).set_counts(
            counts
        ).set_graph_ext(self.graph_ext).generate()
        lines, _ = Fmt.get_size()
        if self.first_loop:
            text = Sentence().add(f"Grafo gerado em graph{self.graph_ext}")
            Fmt.write(lines - 1, 0, text)

    def down_task(self):
        rootdir = self.app.get_rootdir()
        if rootdir == "":
            self.check_root_and_lang()
            return
        lang = self.rep.get_lang()
        if lang == "":
            self.check_root_and_lang()
            return

        obj = self.tree.items[self.tree.index_selected].obj
        if isinstance(obj, Task) and obj.key in obj.title:
            task: Task = obj
            down_frame = (
                Floating("v>").warning().set_ljust_text().set_header(" Baixando tarefa ")
            )
            down_frame.put_text(f"\ntko down {self.rep_alias} {task.key} -l {lang}\n")
            self.fman.add_input(down_frame)

            def fnprint(text):
                down_frame.put_text(text)
                down_frame.draw()
                Fmt.refresh()
            Down.download_problem(self.rep_alias, task.key, lang, fnprint, self.game)
        else:
            if isinstance(obj, Quest):
                self.fman.add_input(
                    Floating("v>")
                    .put_text("\nEssa é uma missão.")
                    .put_text("\nVocê só pode baixar tarefas.\n")
                    .error()
                )
            elif isinstance(obj, Cluster):
                self.fman.add_input(
                    Floating("v>")
                    .put_text("\nEsse é um grupo.")
                    .put_text("\nVocê só pode baixar tarefas.\n")
                    .error()
                )
            else:
                self.fman.add_input(
                    Floating("v>").put_text("\nEssa não é uma tarefa de código.\n").error()
                )
    
    def select_task(self):
        rootdir = self.app.get_rootdir()
        
        obj = self.tree.items[self.tree.index_selected].obj

        if isinstance(obj, Quest) or isinstance(obj, Cluster):
            self.tree.toggle(obj)
            return

        rep_dir = os.path.join(rootdir, self.rep_alias)
        task: Task = obj
        if not task.is_downloadable():
            # self.fman.add_input( Floating().put_text("\nEssa não é uma tarefa de código.\n").error() )
            self.open_link()
            return
        if not task.is_downloaded_for_lang(rep_dir, self.rep.get_lang()):
            self.down_task()
            # self.fman.add_input(
            #     Floating().put_text("\nVocê precisa baixar a tarefa primeiro\n").error()
            # )
            return
        return self.run_selected_task(task, rep_dir)
        
    def run_selected_task(self, task: Task, rep_dir: str):
        path = os.path.join(rep_dir, task.key)
        run = Run([path], None, Param.Basic())
        run.set_lang(self.rep.get_lang())
        run.set_opener(self.opener)
        run.set_autorun(False)
        if Flags.images.is_true():
            run.set_curses(True, Success.RANDOM)
        else:
            run.set_curses(True, Success.FIXED)
        run.set_task(task)

        run.build_wdir()
        if not run.wdir.has_solver():
            msg = Floating("v>").error()
            msg.put_text("\nNenhum arquivo de código na linguagem {} encontrado.".format(self.rep.get_lang()))
            msg.put_text("Arquivos encontrados na pasta:\n")
            folder = run.wdir.get_autoload_folder()
            file_list = [file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]
            for file in file_list:
                msg.put_text(file)
            msg.put_text("")
            self.fman.add_input(msg)
            return
        return run.execute

    def build_list_sentence(self, items: List[Sentence]) -> List[Sentence]:
        out: List[Sentence] = []
        for x in items:
            color_ini = x.data[0].fmt if self.app.is_colored() else "W"
            color_end = x.data[-1].fmt if self.app.is_colored() else "W"
            left = Style.roundL()
            right = Style.roundR()
            middle = x.clone()
            if x.data[0].text == "!":
                left = Style.sharpL()
                right = Style.sharpR()
                middle.data = x.data[1:]
            out.append(Sentence().addf(color_ini.lower(), left).add(middle).addf(color_end.lower(), right))
        return out

    def build_bar_links(self) -> str:
        if not self.tree.items:
            return ""
        obj = self.tree.items[self.tree.index_selected].obj
        if isinstance(obj, Task):
            link = obj.link
            if link:
                return link
        return ""

    def get_task_path(self) -> str:
        obj = self.tree.get_selected()
        if not isinstance(obj, Task):
            return ""
        
        path = os.path.join(self.app.get_rootdir(), self.rep_alias, obj.key, "Readme.md")
        if os.path.isfile(path):
            return path
        return ""
    
    def show_main_bar(self, frame: Frame):
        dy, dx = frame.get_inner()
        top = Sentence()
        if self.two_column_mode() and Flags.others.is_true(): 
            top.add(Style.get_flag_sentence(Flags.config)).add(" ")

        alias_color = "R"
        top.addf(alias_color.lower(), Style.sharpL()).addf(alias_color, self.rep_alias.upper()).addf(alias_color.lower(), Style.sharpR())
        if Flags.others.is_true():
            color = "W" if Flags.admin.is_true() else "K"
            top.add(Style.border_sharp(color, "ADMIN"))
        top.addf("g", Style.sharpL()).addf("G", self.rep.get_lang().upper()).addf("g", Style.sharpR())

        if self.two_column_mode() and Flags.others.is_true(): 
            top.add(" ").add(Style.get_flag_sentence(Flags.skills))

        frame.set_header(top, "^")
        
        if self.two_column_mode():
            elems = self.build_bottom_array()
            line_up = Sentence(" ").join(elems[0 : 2] + elems[-2:])
            frame.set_footer(line_up, "")
        frame.draw()

        for y, sentence in enumerate(self.tree.get_senteces(dy)):
            if sentence.len() > dx:
                sentence.trim_end(dx - 3)
                sentence.addf("r", "...")
            frame.write(y, 0, sentence)

    def show_inventary_bar(self, frame_xp):
        dy, dx = frame_xp.get_inner()
        xp = XP(self.game)
        total_perc = int(
            100 * (xp.get_xp_total_obtained() / xp.get_xp_total_available())
        )
        if Flags.percent.is_true():
            text = f" XPTotal:{total_perc}%"
        else:
            text = f" XPTotal:{xp.get_xp_total_obtained()}"

        done = Style.main_done() + "/"
        todo = Style.main_todo() + "/"
        total_bar = Style.build_bar(text, total_perc / 100, dx - 2, done, todo)
        frame_xp.set_header(Sentence().addf("/", "Skills"), "^", "{", "}")
        frame_xp.set_footer(Sentence().add(" ").add(self.app.get_rootdir()).add(" "), "^")
        frame_xp.draw()



        total, obt = self.game.get_skills_resume([self.game.quests[key] for key in self.game.available_quests])
        elements: List[Sentence] = []
        for skill, value in total.items():
            if Flags.percent.is_true():
                text = f"{skill}:{int(100 * obt[skill] / value)}%"
            else:
                text = f"{skill}:{obt[skill]}/{value}"
            perc = obt[skill] / value
            done = Style.skill_done() + "/"
            todo = Style.skill_todo() + "/"
            skill_bar = Style.build_bar(text, perc, dx - 2, done, todo)
            elements.append(skill_bar)
            
        elements.append(total_bar)

        line_breaks = dy - len(elements)
        for skill_bar in elements:
            frame_xp.print(1, skill_bar)
            if line_breaks > 0:
                line_breaks -= 1
                frame_xp.print(1, Sentence())

    def show_config_bar(self, frame: Frame):
        frame.set_header(Sentence().addf("/", "Config"), "^", "{", "}")
        frame.draw()

        elements: List[Sentence] = []
        pad = 11
        for flag in self.flagsman.left:
            elements.append(Style.get_flag_sentence(flag, pad))


        colored = Flag().name("Colorido").char("C").values(["1" if self.app.is_colored() else "0"]).text("Ativa ou desativa as cores").bool()
        elements.append(Style.get_flag_sentence(colored, pad))
        bordas = Flag().name("Bordas").char("B").values(["1" if self.app.is_nerdfonts() else "0"]).text("Ativa ou desativa as bordas").bool()
        elements.append(Style.get_flag_sentence(bordas, pad))
        
        color = "W" if not self.app.is_colored() else "C"
        elements.append(Sentence().addf(color.lower(), Style.roundL()).addf(color, "DirDestino [D]").addf(color.lower(), Style.roundR()))
        elements.append(Sentence().addf(color.lower(), Style.roundL()).addf(color, "Linguagem  [L]").addf(color.lower(), Style.roundR()))

        # dy, dx = frame.get_inner()
        # line_breaks = dy - len(elements) + 1
        # for i, elem in enumerate(elements):
        #     frame.print(0, elem)
        #     if line_breaks > len(elements) - i - 1:
        #         # line_breaks -= 1
        #         frame.print(0, Sentence())
        dy, dx = frame.get_inner()
        line_breaks = dy - len(elements)
        for i, elem in enumerate(elements):
            frame.print(0, elem)
            if line_breaks > 0:
                line_breaks -= 1
                frame.print(0, Sentence())

    def two_column_mode(self):
        _, cols = Fmt.get_size()
        return cols < self.wrap_size + 2 and Flags.others.is_true()

    def build_bottom_array(self):
        array: List[Sentence] = []
        array += self.help_others_before
        array += self.help_fixed
        if self.app.is_colored():
            color = "G" if Flags.others.is_true() else "Y"
        else:
            color = "W" if Flags.others.is_true() else "K"

        array.append(Sentence() + RToken(color, "!Outros[o]"))
        array += self.help_others_after

        return self.build_list_sentence(array)

    def show_bottom_bar(self):
        lines, cols = Fmt.get_size()
        elems = self.build_bottom_array()
        if self.two_column_mode():
            line_down = Sentence(" ").join(elems[2:-2])
            Fmt.write(lines - 1, 0, line_down.center(cols))
        else:
            if Flags.others.is_true():
                line_all = Sentence(" ").join(elems)
                Fmt.write(lines - 1, 0, line_all.center(cols))
            else:
                line_main = Sentence(" ").join(elems[2: -2]) # alignment adjust
                Fmt.write(lines - 1, 0, line_main.center(cols))   

    def make_xp_button(self, size):
        if self.search_mode:
            text = " Busca: " + self.tree.search_text + "┊"
            percent = 0.0
            done = "W"
            todo = "W"
            text = text.ljust(size)
        else:
            text, percent = self.build_xp_bar()
            done = Style.main_done()
            todo = Style.main_todo()
            text = text.center(size)
        xpbar = Style.build_bar(text, percent, len(text), done, todo)
        return xpbar

    def show_top_bar(self, frame: Frame):
        help = self.build_list_sentence(self.help_basic)
        pesquisar = help[0]
        marcar = help[1]
        config = Style.get_flag_sentence(Flags.config)
        skills = Style.get_flag_sentence(Flags.skills)
        others = Flags.others.is_true()

        pre: List[Sentence] = []
        pre.append(marcar)
        if others and not self.two_column_mode():
            pre.append(config)

        pos: List[Sentence] = []
        if others and not self.two_column_mode():
            pos.append(skills)
        pos.append(pesquisar)

        limit = self.wrap_size
        if frame.get_dx() < self.wrap_size:
            limit = frame.get_dx()
        size = limit - Sentence(" ").join(pre + pos).len() - 2
        main_label = self.make_xp_button(size)
        info = Sentence(" ").join(pre + [main_label] + pos)
        frame.write(0, 0, info.center(frame.get_dx()))


        # frame.set_border_none()
        # frame.set_border_rounded()
        # frame.draw()

    def show_help_config(self):
        _help: Floating = Floating("v>").warning().set_ljust_text().set_header(" Configurações ")
        self.fman.add_input(_help)
        _help.put_sentence(Sentence() + f"      Mínimo " + RToken("r", f"[{Flags.minimum.get_char()}]") + " - Mostrar os requisitos mínimos para completar a missão")
        _help.put_sentence(Sentence() + f"  Recompensa " + RToken("r", f"[{Flags.reward.get_char()}]") + " - Mostrar quanto de experiência cada atividade fornece")
        _help.put_sentence(Sentence() + f"  Percentual " + RToken("r", f"[{Flags.percent.get_char()}]") + " - Mostrar os valores em percentual")
        _help.put_sentence(Sentence() + f"  ModoAdmin " + RToken("r", f"Shift + [A]") + " - Liberar acesso a todas as missões" )
        _help.put_sentence(Sentence() + f"  PastaRaiz " + RToken("r", f"Shift + [{Key.set_root_dir}]") + " - Mudar a pasta padrão de download do tko" )
        _help.put_sentence(Sentence() + f"  Linguagem " + RToken("r", f"Shift + [{Key.set_lang}]") + " - Mudar a linguagem de download dos rascunhos" )


    def show_help(self):
        # def empty(value):
        #     pass
        _help: Floating = Floating("v>").set_ljust_text()
        self.fman.add_input(_help)

        _help.set_header_sentence(Sentence().add(" Ajuda "))
        # _help.put_text(" Movimentação ".center(dx, symbols.hbar.text))
        _help.put_sentence(Sentence("    Ajuda ").addf("r", Key.ajuda).add("  Abre essa tela de ajuda")
        )

        _help.put_sentence(Sentence("  ").addf("r", "Shift + B")
                           .add("  Habilita ").addf("r", "").addf("R", "ícones").addf("r", "").add(" se seu ambiente suportar"))
        _help.put_sentence(Sentence() + "" + RToken("g", "setas") + ", " + RToken("g", "wasd")  + "  Para navegar entre os elementos")
        _help.put_sentence(Sentence() + f"{Actions.ler_online} " + RToken("r", f"{Key.github_open}") + "  Abre tarefa em uma aba do browser")
        _help.put_sentence(Sentence() + f"   {Actions.baixar} " + RToken("r", f"{Key.down_task}") + "  Baixa tarefa de código para seu dispositivo")
        _help.put_sentence(Sentence() + f"   {Actions.editar} " + RToken("r", f"{Key.edit}") + "  Abre os arquivos no editor de código")
        _help.put_sentence(Sentence() + f"   {Actions.ativar} " + RToken("r", "↲") + "  Interage com o elemento")
        _help.put_sentence(Sentence() + f"   {Actions.marcar} " + RToken("r", f"{Key.inc_grade}") + RToken("r", f"{Key.dec_grade}") + " Muda a pontuação da tarefa")
        _help.put_sentence(Sentence())
        _help.put_sentence(Sentence() + "Você pode mudar o editor padrão com o comando")
        _help.put_sentence(Sentence() + RToken("g", "             tko config --editor <comando>"))

    @staticmethod
    def disable_on_resize():
        _, cols = Fmt.get_size()
        if cols < 50 and Flags.skills.is_true() and Flags.config.is_true():
            Flags.skills.toggle()
        elif cols < 30 and Flags.skills.is_true():
            Flags.skills.toggle()
        elif cols < 35 and Flags.config.is_true():
            Flags.config.toggle()


    def build_xp_bar(self) -> Tuple[str, float]:
        xp = XP(self.game)
        if xp.get_xp_total_obtained() == xp.get_xp_total_available():
            text = "Você atingiu o máximo de xp!"
            percent = 100.0
        else:
            # lang = self.rep.get_lang().upper()
            level = xp.get_level()
            percent = float(xp.get_xp_level_current()) / float(xp.get_xp_level_needed())
            if Flags.percent.is_true():
                xpobt = int(100 * xp.get_xp_level_current() / xp.get_xp_level_needed())
                text = "Level:{} XP:{}%".format(level, xpobt)
            else:
                xpobt1 = xp.get_xp_level_current()
                xpobt2 = xp.get_xp_level_needed()
                text = "Level:{} XP:{}/{}".format(level, xpobt1, xpobt2)

        return text, percent

    def show_opening(self):
        if Fmt.get_size()[1] < 100:
            return
        if not Flags.images.is_true():
            return
        _, cols = Fmt.get_size()
        
        now = datetime.datetime.now()
        parrot = random_get(opening, str(now.hour))
        parrot_lines = parrot.split("\n")
        max_len = max([len(line) for line in parrot_lines])
        yinit = 1
        for y, line in enumerate(parrot_lines):
            Fmt.write(yinit + y, cols - max_len - 2, Sentence().addf("g", line))

    def show_items(self):
        border_color = "r" if Flags.admin.is_true() else ""
        Fmt.clear()
        self.tree.reload_sentences()
        lines, cols = Fmt.get_size()
        main_sx = cols  # tamanho em x livre
        main_sy = lines  # size em y avaliable

        top_y = -1
        top_dy = 1  #quantas linhas o topo usa
        bottom_dy = 1 # quantas linhas o fundo usa
        mid_y = top_dy # onde o meio começa
        mid_sy = main_sy - top_dy - bottom_dy # tamanho do meio

        skills_sx = 0
        if Flags.skills.is_true():
            skills_sx = max(20, main_sx // 4)
        else:
            self.show_opening()

        flags_sx = 0
        if Flags.config.is_true():
            flags_sx = 18            

        task_sx = main_sx - flags_sx - skills_sx

        frame_top = Frame(top_y, 0).set_size(top_dy + 2, cols)
        self.show_top_bar(frame_top)

        # frame_bottom = Frame(lines - bottom_dy - 1, -1).set_size(bottom_dy + 2, cols + 2)
        self.show_bottom_bar()
        if task_sx > 5: 
            frame_main = Frame(mid_y, flags_sx).set_size(mid_sy, task_sx).set_border_color(border_color)
            self.show_main_bar(frame_main)

        if Flags.config.is_true():
            frame_flags = Frame(mid_y, 0).set_size(mid_sy, flags_sx).set_border_color(border_color)
            self.show_config_bar(frame_flags)

        if Flags.skills.is_true():
            frame_skills = Frame(mid_y, cols - skills_sx).set_size(mid_sy, skills_sx).set_border_color(border_color)
            self.show_inventary_bar(frame_skills)


    class FlagFunctor:
        def __init__(self, fman: FloatingManager, flag: Flag):
            self.fman = fman
            self.flag = flag

        def __call__(self):
            self.flag.toggle()
            if (self.flag.get_location() == "left" or self.flag.get_location() == "geral") and self.flag.is_bool():
                f = Floating("v>").warning()
                f.put_text("")
                f.put_text(self.flag.get_description())
                if self.flag.is_true():
                    f.put_sentence(Sentence().addf("g", "ligado"))
                else:
                    f.put_sentence(Sentence().addf("r", "desligado"))
                f.put_text("")
                self.fman.add_input(f)

    class GradeFunctor:
        def __init__(self, grade: int, fn):
            self.grade = grade
            self.fn = fn

        def __call__(self):
            self.fn(self.grade)

    def toggle_config(self):
        if Flags.config.is_true():
            Flags.config.toggle()
        else:
            Flags.config.toggle()
            # self.show_help_config()

    def send_quit_msg(self):
        def set_exit():
            self.exit = True

        self.fman.add_input(
            Floating().put_text("\nAté a próxima\n").set_exit_fn(set_exit).warning()
        ),

    def make_callback(self) -> Dict[int, Any]:
        calls: Dict[int, Callable[[],None]] = {}

        def add_int(_key: int, fn):
            if _key in calls.keys():
                raise ValueError(f"Chave duplicada {chr(_key)}")
            calls[_key] = fn

        def add_str(str_key: str, fn):
            if str_key != "":
                add_int(ord(str_key), fn)

        add_int(curses.KEY_RESIZE, self.disable_on_resize)
        add_str(Key.quit, self.send_quit_msg)
        add_int(27, self.send_quit_msg)
        add_int(curses.KEY_BACKSPACE, self.send_quit_msg)


        add_str(Key.up, self.tree.move_up)
        add_int(curses.KEY_UP, self.tree.move_up)

        add_str(Key.down, self.tree.move_down)
        add_int(curses.KEY_DOWN, self.tree.move_down)

        add_str(Key.left, self.tree.arrow_left)
        add_int(curses.KEY_LEFT, self.tree.arrow_left)

        add_str(Key.right, self.tree.arrow_right)
        add_int(curses.KEY_RIGHT, self.tree.arrow_right)

        add_str(Key.ajuda, self.show_help)
        add_str(Key.expand, self.tree.process_expand)
        add_str(Key.expand2, self.tree.process_expand)
        add_str(Key.collapse, self.tree.process_collapse)
        add_str(Key.collapse2, self.tree.process_collapse)
        add_str(Key.github_open, self.open_link)
        add_str(Key.set_lang, lambda: self.set_language(False))
        add_str(Key.set_root_dir, lambda: self.set_rootdir(False))
        add_str(Key.down_task, self.down_task)
        add_str(Key.select_task, self.select_task)
        add_str("t", lambda: self.fman.add_input(Floating().put_text("\n Use o Enter para testar uma questão\n").warning()))
        add_str(Key.inc_grade, self.tree.inc_grade)
        add_str(Key.inc_grade2, self.tree.inc_grade)
        add_str(Key.dec_grade, self.tree.dec_grade)
        add_str(Key.dec_grade2, self.tree.dec_grade)
        add_str(Key.edit, lambda: self.opener.open_code(open_dir=True))
        add_str(Key.cores, self.app.toggle_color)
        add_str(Key.bordas, self.app.toggle_nerdfonts)

        for value in range(1, 10):
            add_str(str(value), self.GradeFunctor(int(value), self.tree.set_grade))
        add_str("'", self.GradeFunctor(0, self.tree.set_grade))
        add_str("0", self.GradeFunctor(10, self.tree.set_grade))

        for flag in self.flagsman.left:
            add_str(flag.get_char(), self.FlagFunctor(self.fman, flag))
        for flag in self.flagsman.others:
            add_str(flag.get_char(), self.FlagFunctor(self.fman, flag))

        add_str(Flags.config.get_char(), self.toggle_config)
        add_str(Flags.skills.get_char(), self.FlagFunctor(self.fman, Flags.skills))
        add_str("/", self.toggle_search)

        return calls

    def toggle_search(self):
        self.search_mode = not self.search_mode
        if self.search_mode:
            self.backup_expanded = [v for v in self.tree.expanded]
            self.backup_index_selected = self.tree.index_selected
            self.backup_admin_mode = Flags.admin.is_true()
            self.tree.update_tree(admin_mode=True)
            self.tree.process_expand()
            self.tree.process_expand()
            self.fman.add_input(Floating(">v").warning().put_text("Digite o texto\nVavegue até o elemnto desejado\ne aperte Enter"))
    
    def finish_search(self):
        self.search_mode = False
        unit = self.tree.get_selected()
        self.tree.index_selected = 0
        self.tree.search_text = ""
        if self.backup_admin_mode == False:
            self.tree.update_tree(admin_mode=False)
        self.tree.reload_sentences()
    
        found = False
        for i, item in enumerate(self.tree.items):
            if item.obj == unit:
                self.tree.index_selected = i
                found = True
                break

        if not found:
            self.fman.add_input(Floating(">v").warning().put_text("Elemento não acessível no modo normal.\nEntrando no modo Admin\npara habilitar acesso"))
            Flags.admin.toggle()
            self.tree.update_tree(True)
            self.tree.reload_sentences()
        
        self.tree.process_collapse()
        self.tree.process_collapse()

        if isinstance(unit, Task):
            for cluster_key in self.game.available_clusters:
                cluster = self.game.clusters[cluster_key]
                for quest in cluster.quests:
                    for task in quest.get_tasks():
                        if task == unit:
                            self.tree.expanded = [cluster.key, quest.key]
        elif isinstance(unit, Quest):
            for cluster_key in self.game.available_clusters:
                cluster = self.game.clusters[cluster_key]
                for quest in cluster.quests:
                    if quest == unit:
                        self.tree.expanded = [cluster.key]
        self.tree.reload_sentences()
        for i, item in enumerate(self.tree.items):
            if item.obj == unit:
                self.tree.index_selected = i
                break


    def process_search(self, key):
        if key == 27:
            self.search_mode = False
            self.tree.search_text = ""
            self.tree.expanded = [v for v in self.backup_expanded]
            self.tree.index_selected = self.backup_index_selected
        elif key == ord("\n"):
            self.finish_search()
    
        elif key == curses.KEY_UP:
            self.tree.move_up()
        elif key == curses.KEY_DOWN:
            self.tree.move_down()
        elif key == 127 or key == 263 or key == 330:
            self.tree.search_text = self.tree.search_text[:-1]
        elif key >= 32 and key < 127:
            self.tree.search_text += chr(key).lower()
        

    def send_char_not_found(self, key):
        self.fman.add_input(
            Floating("v>")
                .error()
                .put_text("Tecla")
                .put_text(f"char {chr(key)}")
                .put_text(f"code {key}")
                .put_text("não reconhecida")
                .put_text("")
        )

    # def send_dont_use_enter(self):
    #     self.fman.add_input(
    #         Floating("v>")
    #             .put_text("\n")
    #             .put_text("Utilize esquerda e direita\npara marcar as questões")
    #             .put_text("e compactar e expandir tópicos \n")
    #             .put_text("")
    #     )

    def main(self, scr):
        if hasattr(curses, "set_escdelay"):
            curses.set_escdelay(25)
        else:
            os.environ.setdefault('ESCDELAY', '25')
        # verify if curses has method set_escdelay
        curses.curs_set(0)  # Esconde o cursor
        Fmt.init_colors()  # Inicializa as cores
        Fmt.set_scr(scr)  # Define o scr como global

        while not self.exit:
            self.tree.update_tree(admin_mode=Flags.admin.is_true() or self.search_mode)
            self.fman.draw_warnings()
            self.generate_graph()
            calls = self.make_callback()
            self.show_items()

            if self.fman.has_floating():
                value: int = self.fman.get_input()
            else:
                value = scr.getch()
                if value == 195:
                    value = scr.getch()
                    if value == 167: #ç
                        value = ord("c")

            if self.search_mode:
                self.process_search(value)
            elif value in calls.keys():
                callback = calls[value]()
                if callback is not None:
                    return callback
            elif value != -1 and value != 27:
                self.send_char_not_found(value)

            self.tree.reload_sentences()
            self.save_to_json()
            if self.first_loop:
                self.first_loop = False

    def check_lang_in_text_mode(self):
        lang = self.rep.get_lang()
        if lang == "":
            options = languages_avaliable
            print("\nLinguagem padrão ainda não foi definida.\n")
            while True:
                print("Escolha entre as opções a seguir ", end="")
                print("[" + ", ".join(options) + "]", ":", end=" ")
                lang = input()
                if lang in options:
                    break
            self.rep.set_lang(lang)

    def play(self, graph_ext: str):
        self.graph_ext = graph_ext
        self.check_lang_in_text_mode()

        while True:
            output = curses.wrapper(self.main)
            if output is None:
                return
            else:
                output()
