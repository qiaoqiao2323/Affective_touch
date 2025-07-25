#!/bin/bash
source /usr/local/src/robot/robotology-superbuild/build/install/share/ICUBcontrib/contexts/icubDemos/icub_basics.sh

#######################################################################################
# "MAIN" DEMOS:                                                                       #
#######################################################################################


robot_show_off() {
    breathers "stop"

    # 🤸 开场：体操动作
    speak "\rspd=85\ Il mio corpo è molto flessibile. Posso anche fare un po’ di ginnastica!"
    sleep 1.0

    moving_torso_right 2.0
    speak "Verso destra..."
    moving_torso_left 2.0
    speak "E ora verso sinistra..."
    moving_torso_right 2.0
    speak "Ancora un po’ di movimento!"
    moving_torso_left 2.0

    go_home
    sleep 1.0

    # 💪 展示“肌肉”
    speak "\rspd=85\ E se vuoi vedere quanto sono forte..."
    mostra_muscoli
    sleep 1.0
    speak "Guarda!"

    right_up_left_down
    sleep 1.0
    speak "Braccio destro su!"

    left_up_right_down
    sleep 1.0
    speak "Ora il sinistro!"

    opposite_muscles
    sleep 1.0
    speak "Tutti e due!"

    go_home
    sleep 2.0
    breathers "start"
}



introskin(){
	start_face_tracker
	guarda_c
	sleep 1.0
	ciao_gesto
	speak "Ciao! Sono il robot iCub e mi chiamo Berry. È un vero piacere conoscerti."
	#sleep 3.0
	#speak "I ricercatori I I T mi hanno dotato di strumenti per interagire con gli esseri umani."
	#sleep 2.0
	explain_eyes
	sleep 2.0
	present_nose
	#sleep 5.0
	robot_show_off
	sleep 1.0
	present_emotions
	sleep 2.0
	# Start speaking rules
	speak "Ti ringrazio per aver deciso di partecipare a questo studio sul tocco emotivo."
	sleep 2.0
	speak "In questo esperimento, vogliamo esplorare come le persone esprimono le emozioni attraverso il tocco quando interagiscono con un robot come me."
	sleep 2.0
  	speak "Ora ti spiegherò le regole del nostro esperimento."
  	sleep 1.0
  	speak "Inizierai con una sessione di esplorazione: in questa fase sei libero di toccarmi come preferisci. Premi ‘t’ per iniziare a toccarmi e ‘s’ se desideri interrompere."
  	speak "Successivamente, prenderai parte all’esperimento principale."
  	speak "Che consiste in tre sessioni, quindi in totale completerai nove turni."
  	speak "In ogni turno, il tuo compito è usare il tocco per esprimere otto emozioni diverse nei miei confronti."
  	sleep 2.0
  	speak "In ogni turno esprimerai tutte e otto le emozioni, una alla volta, e ogni interazione di tocco durerà circa 10 secondi."
  	sleep 2.0
 	speak "All'inizio di ogni prova, ti dirò quale emozione dovrai esprimere."
 	speak "Dopo ogni espressione, ti ricorderò che il tempo è terminato, e potrai anche vedere un conto alla rovescia sullo schermo."
	sleep 2.0
	speak "Poi passeremo all'emozione successiva. Prima dell’inizio di ogni sessione, avrai un momento per prepararti e pensare a come desideri esprimere ciascuna emozione."
	sleep 2.0
	speak "Non c’è un modo giusto o sbagliato—usa semplicemente il tocco che per te è più naturale."
  	speak "Se non ti ricordi tutte le regole, non preoccuparti: ti verranno fornite anche su carta e saranno visibili sullo schermo più avanti."
  	sleep 1.0
  	speak "E naturalmente, se in qualsiasi momento ti senti a disagio o hai bisogno di una pausa, puoi fermarti,"
  	speak "saltare una prova o interrompere l’esperimento in qualsiasi momento."
  	sleep 2.0
  	speak "Ti basta avvisare l'esperimentatore. Il tuo benessere è molto importante per noi."
	saluta
	sleep 2.0
	speak "Iniziamo!"
	stop_face_tracker
	go_home_human
	breathers "stop"
    }



Ciao! Sono il robot iCub e mi chiamo Berry. È un vero piacere conoscerti, e ti ringrazio per aver deciso di partecipare a questo studio sul tocco emotivo. In questo esperimento, vogliamo esplorare come le persone esprimono le emozioni attraverso il tocco quando interagiscono con un robot come me.
Parteciperai prima a una sessione di esplorazione: in questa fase, sei libero di toccarmi in qualsiasi parte, dalla testa, al corpo, fino ai piedi, come preferisci. Premi ‘t’ per iniziare a toccarmi e ‘s’ se desideri interrompere il contatto. Dopo l’esplorazione, prenderai parte all’esperimento principale, che è composto da tre sessioni. Ogni sessione include tre turni, quindi in totale completerai nove turni. In ogni turno, esprimerai otto emozioni (sette emozioni più un’intenzione), una alla volta. Ogni interazione tramite il tocco durerà circa 10 secondi. All’inizio di ogni prova, ti dirò quale emozione dovrai esprimere. Dopo ogni espressione, ti ricorderò che il tempo è terminato e vedrai anche un conto alla rovescia sullo schermo. Poi passeremo all’emozione successiva. Nella prima sessione, come nella fase di esplorazione, potrai toccarmi liberamente in qualsiasi parte, dalla testa ai piedi. Ti darò ulteriori istruzioni al termine della prima sessione. Prima dell’inizio di ogni sessione, avrai un momento per prepararti e pensare a come desideri esprimere ogni emozione. Non c’è un modo giusto o sbagliato—usa semplicemente il tocco che ti viene naturale.
Se non ti ricordi tutte le regole, non preoccuparti: ti verranno fornite anche su carta e saranno visibili sullo schermo più avanti. E naturalmente, se in qualsiasi momento ti senti a disagio o hai bisogno di una pausa, puoi fermarti, saltare una prova o interrompere l’esperimento in qualsiasi momento. Ti basta avvisare l'esperimentatore. Il tuo benessere è molto importante per noi. Iniziamo! 
#######################################################################################
# "MAIN" FUNCTION:                                                                    #
#######################################################################################
list() {
	compgen -A function
}


echo "********************************************************************************"
echo ""

$1 "$2"

if [[ $# -eq 0 ]] ; then 
    echo "No options were passed!"
    echo ""
    usage
    exit 1
fi

