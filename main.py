
import os.path
from re import I
import customtkinter as ctk 
import customtkinter 
from PIL import Image,ImageTk
from capas import backgroud
from pygame import mixer
import pygame
from capas import titulo
from time import sleep
from customtkinter import filedialog
import tkinter
atualizador=''
class MyFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):# falta configurar os botoes de cada musica pra reproduzir
        super().__init__(master, **kwargs)
        
        # add widgets onto the frame...
        mixer.init()
        self.label = customtkinter.CTkLabel(self,text='',height=69)
        self.label.grid(row=0, column=0, padx=20)
        self.n4=40
        self.meuovo=0
        self.teste()
        tamanho=69*len(self.n2)
        self.label.configure(height=tamanho)
        self.criar()
        if len(self.n2)>0:
            while len(self.n2)>0:
                self.criar()
                
    def teste(self):
        
        n1=open('caminhos.txt','r')
        self.n2=list()
        self.dici=dict()
        
        for c in n1.readlines():
            self.n1=c.replace('\n','')
            
            n3=titulo.info(self.n1)[2]
            
            self.n2.append(n3)
            self.dici[n3]=self.n1
    def criar(self):
        
        try:
            nome_musica=self.n2.pop()
            try:
                
                mixer.music.load(self.dici[nome_musica])
                self.n1=customtkinter.CTkButton(self,text=nome_musica,width=400,command=lambda:(mixer.music.unload(),mixer.music.load(self.dici[nome_musica]),(mixer.music.play()),(self.atualizador(self.dici[nome_musica]))))
                self.n1.place(x=-5,y=self.n4)
                
                self.n4+=27
            except:
                self.criar()
            
        except:
            return
    def atualizador(self,dici):
        global atualizador
        atualizador=dici
class musica_window(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.my_frame = MyFrame(master=self, width=410, height=200, corner_radius=0,fg_color='#242424')
        self.my_frame.grid(row=0, column=0, sticky="nsew")
        self.geometry("400x400")
        self.resizable(width=False,height=False)
        self.config(background='#242424') 
        
        #self.title('Musicas')
class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.geometry("550x350")
        self.config(background='#242424')
        self.resizable(width=False,height=False)
        self.tabview()
        self.title('configuraçao')
    def tabview(self):
        tabview = customtkinter.CTkTabview(master=self,
                                            anchor='nw',
                                            fg_color='#242424',
                                            width=500,height=330,
                                            border_width=2,
                                            border_color='gray',
                                            segmented_button_selected_color='#242424',
                                            bg_color='#242424',
                                            segmented_button_fg_color='#242424',
                                            
                                            segmented_button_unselected_hover_color='black',#cor de quando passa o mouse
                                            corner_radius=10)
        tabview.place(x=25,y=10)
        tabview.add("sobre")  
        tabview.set("sobre") 

        #nome do programa
        victory=customtkinter.CTkLabel(master=tabview.tab('sobre'),text='victory-rhythm',text_color='purple',font=customtkinter.CTkFont(size=15))
        victory.place(x=190,y=110)
        #versao do programa
        versao=customtkinter.CTkLabel(master=tabview.tab('sobre'),text='1.0 alpha ',text_color='gray')
        versao.place(x=190,y=140)
        #icone 
        imagem_icone=customtkinter.CTkImage(Image.open('imagens/icone_app.png'),size=(100,100))
        icone=customtkinter.CTkLabel(master=tabview.tab('sobre'),text='',image=imagem_icone)
        icone.place(x=190,y=0)
        #aquele textinho sobre o projeto
        texto_sobre=customtkinter.CTkLabel(master=tabview.tab('sobre'),font=customtkinter.CTkFont(size=15),text_color='white',text='''ola, esse e o meu primeiro projeto com o customtkinter e python,
espero que tenha gostado,se esse projeto te interesou
e vc quiser aconpanhar esse projeto ou outros e so
acessar meu github ''')
        texto_sobre.place(x=33,y=170)

        git=customtkinter.CTkImage(Image.open('imagens/git.png'),size=(50,40))
        botao_git=customtkinter.CTkButton(master=tabview.tab('sobre'),image=git,text='',fg_color='#242424',width=10,height=10)
        botao_git.place(x=400,y=230)
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        global atualizador
        mixer.init()
        self.geometry('400x600')
        self.config(background='#242424')
        self.title('player')
        self.resizable(width=False,height=False)   #aqui evita que a tela seja redimesionada
        self.variaveis_funçoes()
        self.funçoes_iniciais()
        self.subtitulo()
        self.atualizador()
        
    def atualizador(self):# aqui esta tendo um bug de a musica atual esta tendo uma duplicata por causa do atualizador 
        global atualizador
        if self.musica_window is None or not self.musica_window.winfo_exists():
            self.after(1000,self.atualizador)
        else:
            pass
            if atualizador!=self.musica_atual:
                if atualizador=='':
                    atualizador=self.musica_atual
                else:    
                    self.musica_atual=atualizador
                self.back=customtkinter.CTkImage(titulo.capa(self.musica_atual),size=(300,300)) 
                self.imagem_fundo.configure(self,text='',image=self.back)
                self.imagem_fundo.place_configure(x=50,y=50)
                #aqui reseta os segundos e os minutos do update label
                self.segundos=self.minutos=0
            #atualiza o titulo da janela
                self.titulo_atual=titulo.info(self.musica_atual)[1]
                self.title(self.titulo_atual)
            #aqui atualiza a duraçao da barra 
                self.duraçao=titulo.info(musica=self.musica_atual)[0]
                self.progresso.set(0)
                self.barra.configure(variable=self.progresso,to=self.duraçao)
                self.autor=titulo.info(self.musica_atual)[2]
                self.sub_titulo.configure(text=self.autor)
                self.after(1000,self.atualizador) 
            else:
                self.after(1000,self.atualizador) 
    def funçoes_iniciais(self):
        self.botao() 
        self.label()
        self.backgroud()
        self.variavel_do_total()
        self.update_total()
        self.update_barra()
        self.update_label()
        self.botao_play()
        self.player(self.musica_atual)
        self.botao_janela()
        self.volume()
    def variaveis_funçoes(self):
        self.segundos=self.minutos=self.hora=0
        self.image_button=customtkinter.CTkButton(master=self,text='')
        self.image_button.place(x=182,y=470)
        self.musica_atual='kendrik.mp3'
        self.progresso=customtkinter.IntVar()
        self.vari=0
        self.n1=1#aqui ativa o botao play
        self.caminhos=list()
        self.end_event=0
        caminho=open('caminhos.txt','r+')
        if caminho.readable():
            for c in caminho.readlines():
                
                self.caminhos.append(c)
                
        else:
            self.abrir_pastas()   
        self.musica_proxima=list(self.caminhos.copy())
        #print(self.musica_proxima)
        self.musica_anterior=list()
        
        #self.titulo_atual=titulo.info(self.musica_atual)[1]
        #self.title(self.titulo_atual)
        
        self.variavel_volume=customtkinter.DoubleVar(value=0.55)
        self.barra_volume=customtkinter.CTkSlider(self,from_=0,
                                        to=1,
                                    width=100,
                                    border_color='#242424',
                                    bg_color='#242424',variable=self.variavel_volume,
                                    )
        self.barra_volume.place(x=20,y=20)
    def backgroud(self):
        self.back=customtkinter.CTkImage(titulo.capa(self.musica_atual),size=(300,300)) 
        self.imagem_fundo=customtkinter.CTkLabel(self,text='',image=self.back)
        self.imagem_fundo.place(x=50,y=50)
    def player(self,musica):#tudo ok por aqui
        mixer.init()
        try:
            mixer.music.load(musica)
        except:
            self.proximo()
            return    
        mixer.music.play()
        evento=pygame.USEREVENT + 1
        mixer.music.set_endevent(evento)
    def pausar(self):#tudo ok por aqui
        mixer.music.pause()
    def despausar(self):#tudo ok por aqui
        mixer.music.unpause()    
    def botao(self):#tudo ok por aqui
        #botao anterior
        botao_a = customtkinter.CTkImage(Image.open("/home/danields/Desktop/projetos/player_musica/imagens/anterior.png"),
                                                    size=(41, 28))
        botao_anterior=ctk.CTkButton(self,image=botao_a,
                                    width=10,
                                    height=10,
                                    text='',
                                    fg_color='#242424',
                                    bg_color='#242424',
                                    command=self.anterior)
        botao_anterior.place(x=114,y=470)
        #botao proximo
        botao_p = customtkinter.CTkImage(Image.open("/home/danields/Desktop/projetos/player_musica/imagens/proximo.png"),
                                                    size=(41,28))
        botao_proximo=ctk.CTkButton(self,text='',
                                    image=botao_p,
                                    width=10,
                                    height=10,
                                    fg_color='#242424',
                                    bg_color='#242424',
                                    command=self.proximo)
        botao_proximo.place(x=231,y=470)       
    def botao_play(self):# aqui esta ok 
        n1=self.n1
        
        self.image_button.destroy()
        if n1%2==0:
            self.pausar()
            self.button_image = customtkinter.CTkImage(Image.open("/home/danields/Desktop/projetos/player_musica/imagens/play1.png"), size=(30, 30)) 
            self.image_button = customtkinter.CTkButton(master=self,
                                                anchor='center',
                                                image=self.button_image,
                                                width=10,
                                                height=10,
                                                text='',
                                                fg_color='#242424',
                                                command=self.atualizador,
                                                bg_color='#242424')
            
            self.n1+=1
            self.image_button.place(x=182,y=470)
            
        else:
            self.despausar()
            self.button_image = customtkinter.CTkImage(Image.open("/home/danields/Desktop/projetos/player_musica/imagens/pause.png"), size=(32, 32))
            self.image_button = customtkinter.CTkButton(master=self,
                                                anchor='center',
                                                text="",
                                                image=self.button_image,
                                                width=10,
                                                height=10,
                                                corner_radius=50,
                                                bg_color='#242424',
                                                command=self.atualizador)
            
            self.n1+=1
            self.image_button.place(x=182,y=470)      
    def label(self):# aqui esta tudo ok
        self.texto=ctk.CTkLabel(self,text='',bg_color='#242424',text_color='black')
        self.texto.place(x=50,y=450)
    def update_label(self,segundos=0,hora=0,minutos=0):#aqui esta tudo ok
        if mixer.music.get_busy():
            #aqui vai adicionar os segundos e a variavel da barra e tentar deixar sicronizado um com o outro
            self.segundos+=1
            self.vari=self.progresso.get()
            self.vari+=1
            self.progresso.set(self.vari)

            self.end_event=self.progresso.get()
            if self.end_event>=self.duraçao:# aqui vai verificar o termino da musica com base na barra 
                self.proximo()
            
        else:
            self.end_event=self.progresso.get()
            if self.end_event>=self.duraçao:# aqui vai verificar o termino da musica com base na barra 
                self.proximo()
            
            pass
        if self.segundos==60:
            self.segundos=0
            self.minutos+=1
        elif self.segundos>60:
            while self.segundos>60:
                self.segundos-=60
                self.minutos+=1 
        if self.segundos<10 and self.minutos<10:
            self.texto.configure(text = f'0{self.hora}:0{self.minutos}:0{self.segundos}\r')
        elif self.segundos<10 and self.minutos>=10:
            self.texto.configure(text = f'0{self.hora}:{self.minutos}:0{self.segundos}')
        elif self.segundos>=10 and self.minutos<10:
            self.texto.configure(text = f'0{self.hora}:0{self.minutos}:{self.segundos}')
        elif self.segundos>=10 and self.minutos>=10:
            self.texto.configure(text = f'0{self.hora}:{self.minutos}:{self.segundos}')
        
        
        self.texto.after(1000,self.update_label) # chama este método novamente em 1.000 milissegundos  
    def variavel_do_total(self):
        self.total=ctk.CTkLabel(self,text='',bg_color='#242424',text_color='black')
        self.total.place(x=300,y=450)
    def update_total(self):#aqui esta tudo ok
        #duraçao total da musica
        self.duraçao=titulo.info(musica=self.musica_atual)[0]
        segundos_total=self.duraçao
        minutos_total=0
        horas_total=0
        
        if segundos_total==60:
            segundos_total=0
            minutos_total+=1
        elif segundos_total>60:
            while segundos_total>60:
                segundos_total-=60
                minutos_total+=1 
        if segundos_total<10 and minutos_total<10:
            self.total.configure(text = f'0{horas_total}:0{minutos_total}:0{segundos_total}')
        elif segundos_total<10 and minutos_total>=10:
            self.total.configure(text = f'0{horas_total}:{minutos_total}:0{segundos_total}')
        elif segundos_total>=10 and minutos_total<10:
            self.total.configure(text = f'0{horas_total}:0{minutos_total}:{segundos_total}')
        elif segundos_total>=10 and minutos_total>=10:
            self.total.configure(text = f'0{horas_total}:{minutos_total}:{segundos_total}')
        #self.total.after(1000,self.update_total)    
    def abrir_pastas(self):
        try:
            self.abrir_diretorio=filedialog.askdirectory(title='abra a pasta de suas musicas')
            self.variavel_do_verificador(self.abrir_diretorio)
        except:
            print('erro nas pastas')    
    def tirar_musica(self):#tudo ok por aqui
        mixer.music.unload()   
    def reiniciar_musica():#tudo ok por aqui
        mixer.music.rewind()    
    def proximo(self):#tudo ok por aqui
        global atualizador
        if len(self.musica_proxima)>=1:
            #print(len(self.musica_proxima))
            try:
                if len(self.musica_proxima)!=0:
                    self.musica_anterior.append(self.musica_atual)
                    self.tirar_musica()
                    self.musica_atual=str(self.musica_proxima.pop())
                if '\n' in self.musica_atual:
                    self.musica_atual=self.musica_atual.replace('\n','')
                try:
                    mixer.music.load(self.musica_atual)
                    #print(self.musica_atual)
                    pygame.mixer.music.play()
                except:
                    print('erro no load ')
                    self.proximo()
                if self.n1%2==0:
                    pass
                else:
                    self.botao_play()
                self.update_total()
               
            #aqui serve pra atualizar a capa das musicas
                atualizador=self.musica_atual
                self.back=customtkinter.CTkImage(titulo.capa(self.musica_atual),size=(300,300)) 
                self.imagem_fundo.configure(self,text='',image=self.back)
                self.imagem_fundo.place_configure(x=50,y=50)
                print(self.musica_atual)
                print(atualizador)
                print('oie')
            #aqui reseta os segundos e os minutos do update label
                self.segundos=self.minutos=0
            #atualiza o titulo da janela
                self.titulo_atual=titulo.info(self.musica_atual)[1]
                self.title(self.titulo_atual)
            #aqui atualiza a duraçao da barra 
                self.duraçao=titulo.info(musica=self.musica_atual)[0]
                self.progresso.set(0)
                self.barra.configure(variable=self.progresso,to=self.duraçao)
            

                self.autor=titulo.info(self.musica_atual)[2]
                self.sub_titulo.configure(text=self.autor)
            except IndexError:
                print('sem musica')
                print('='*50)
           # print(self.musica_anterior)
                print('='*50)
            #print(self.musica_atual)
        else:
            print('sem musica')    
    def anterior(self):
        try:
            if len(self.musica_anterior)!=0:
                self.musica_proxima.append(self.musica_atual)
                self.tirar_musica()    
                self.musica_atual=str(self.musica_anterior.pop())
            if '\n' in self.musica_atual:
                self.musica_atual=self.musica_atual.replace('\n','')
            try:
                mixer.music.load(self.musica_atual)
                pygame.mixer.music.play()
            except:
                print('erro no load')
                self.anterior()
            if self.n1%2==0:
                pass
            else:
                self.botao_play()

            #if len(self.musica_anterior)!=0: #and len(anterior)!=0:
            #    self.musica_proxima.append(self.musica_atual)
           # self.musica_atual=self.musica_anterior.pop()
           # pygame.mixer.music.load(self.musica_atual)
           # pygame.mixer.music.play()
           # if self.n1%2==0:
           ### else:
           #     self.botao_play()  
            self.update_total()    

            #pega a nova capa e coloca
            self.back=customtkinter.CTkImage(titulo.capa(self.musica_atual),size=(300,300)) 
            self.imagem_fundo.configure(self,text='',image=self.back)
            self.imagem_fundo.place_configure(x=50,y=50)
            #reseta os segundos 
            self.segundos=self.minutos=self.hora=0
            #atualiza o titulo da janela
            self.titulo_atual=titulo.info(self.musica_atual)[1]
            self.title(self.titulo_atual)
            #aqui atualiza a duraçao da barra
            self.duraçao=titulo.info(musica=self.musica_atual)[0]
            self.progresso.set(0)
            self.barra.configure(to=self.duraçao,variable=self.progresso)


            self.autor=titulo.info(self.musica_atual)[2]
            self.sub_titulo.configure(text=self.autor)
        except IndexError:
            print('sem musica')   
            print('='*50) 
            #print(self.musica_proxima)
            print('='*50)
            #print(self.musica_atual)  
    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()
    def botao_janela(self):  
        #imagem=customtkinter.CTkImage(Image.open('/home/danields/Desktop/projetos/player_musica/imagens/ponto.png'), size=(30,30))
        #self.button_1 = customtkinter.CTkButton(self, text="", command=self.open_toplevel,width=15,height=15,image=imagem,fg_color='#242424',bg_color='#242424')
        #self.button_1.place( x=360, y=10)
        self.musica_window= None
        self.toplevel_window = None 
        def optionmenu_callback(opcoes):
            if opcoes=='Opçoes':
                pass
            elif opcoes=='Musicas':
                self.musicas()
            elif opcoes=='Adicionar musica':
                self.abrir_pastas()
            else:
                self.open_toplevel()   
        optionmenu = customtkinter.CTkOptionMenu(master=self, values=["Opçoes","Musicas",'Adicionar musica',"Geral"],width=50,
                                            command=optionmenu_callback,bg_color='#242424')
        optionmenu.set("opçoes")
        optionmenu.place(x=320,y=10)
    def musicas(self):
        if self.musica_window is None or not self.musica_window.winfo_exists():
            self.musica_window = musica_window(self)
            
            self.atualizador()  # create window if its None or destroyed
        else:
            self.musica_window.focus()  # if window exists focus it
    def update_barra(self):#tudo ok
        #infomaçoes da barra
        self.vari=self.progresso.get()
        #print(self.progresso.get())
        self.vari+=1
        self.progresso.set(self.vari)
        #print(self.vari)
        
        self.barra=customtkinter.CTkSlider(self,from_=0,
                                    to=self.duraçao,
                                    width=360,
                                    variable=self.progresso,
                                    border_color='#242424',
                                    bg_color='#242424'
                                    ,command=lambda n1:self.progresso_atual())
        self.barra.place(x=20,y=430)
    def volume_barra(self):
        self.barra=customtkinter.CTkSlider(self,from_=0,
                                    to=1.0,
                                    width=360,
                                    variable=self.progresso,
                                    border_color='#242424',
                                    bg_color='#242424'
                                    ,)
        self.barra.place(x=20,y=430)    
    def progresso_atual(self):
        self.progresso.set(self.progresso.get())
        if mixer.music.get_busy():
            mixer.music.set_pos(self.progresso.get())
            self.segundos=self.minutos=self.horas=0
            
            self.segundos=self.progresso.get()
            self.segundos+=1
            self.vari=self.progresso.get()
            self.vari+=1
            self.progresso.set(self.vari)
            #print(self.vari,self.segundos)
        else:
            pass
        if self.segundos==60:
            self.segundos=0
            self.minutos+=1
        elif self.segundos>60:
            while self.segundos>60:
                self.segundos-=60
                self.minutos+=1 
        if self.segundos<10 and self.minutos<10:
            self.texto.configure(text = f'0{self.hora}:0{self.minutos}:0{self.segundos}\r')
        elif self.segundos<10 and self.minutos>=10:
            self.texto.configure(text = f'0{self.hora}:{self.minutos}:0{self.segundos}')
        elif self.segundos>=10 and self.minutos<10:
            self.texto.configure(text = f'0{self.hora}:0{self.minutos}:{self.segundos}')
        elif self.segundos>=10 and self.minutos>=10:
            self.texto.configure(text = f'0{self.hora}:{self.minutos}:{self.segundos}')
    def subtitulo(self):#
        self.autor=titulo.info(self.musica_atual)[2]
        self.sub_titulo=customtkinter.CTkLabel(self,text=self.autor,font=customtkinter.CTkFont(size=15),fg_color='#242424',text_color='black',width=400)
        self.sub_titulo.place(x=00,y=400)
    def volume(self):#oi
        
        mixer.music.set_volume(self.variavel_volume.get())
        self.after(1000,self.volume)
    def verificador(self):
        for c in self.n1:
            junçao=self.caminhos+'/'+c
            if os.path.isfile(junçao):
                self.arquivos.append(junçao)
            elif os.path.isdir(junçao):
                self.pastas.append(junçao)
    def separador(self):
        for c in self.arquivos:
            if '.mp3' in c :
                self.mp3.add(c)
    def variavel_do_verificador(self,pasta):
        self.caminhos=pasta
        self.n1=os.listdir(self.caminhos)
        self.arquivos=list()
        self.pastas=list()
        self.mp3=set()
        self.arquivo_aleatorio=list()
        self.verificador()
        self.separador()
        while len(self.pastas)>0:
            self.caminhos=self.pastas.pop()
            self.n1=os.listdir(self.caminhos)
            self.verificador()
            self.separador()
        try:    
            caminho=open('caminhos.txt','r+')
        except FileNotFoundError:
            caminho=open('caminhos.txt','w+')
        finally:
            for c in self.mp3:
                caminho.writelines(c)
                caminho.writelines('\n')
        caminho.close()
        self.impedir_duplicatas()  
        self.sobrescrever()     
    def impedir_duplicatas(self):
        try:
            caminho=open('caminhos.txt','r+')
        except FileNotFoundError:
            caminho=open('caminhos.txt','w+')
        try:
            open_dupli=open('duplicata.txt','r+')
        except FileNotFoundError:
            open_dupli=open('duplicata.txt','w+')
        duplicata=set()
        caminho.close()
        caminho=open('caminhos.txt','r+')
        for c in caminho.readlines():
            #print(c)# nao sei porque colocquei
            if c=='\n':
                pass
            elif '\n' in c:
                duplicata.add(c)
            else:
                c=c+'\n'
                duplicata.add(c)
        
        for c in duplicata:
            open_dupli.writelines(c)
        caminho.close()
        open_dupli.close()        
    def sobrescrever(self):
        caminho=open('caminhos.txt','w+')  
        open_dupli=open('duplicata.txt','r+')
        for c in open_dupli:
            caminho.writelines(c)        
app=App()
app.mainloop()

