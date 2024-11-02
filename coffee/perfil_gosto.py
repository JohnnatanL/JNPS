import streamlit as st
import pandas as pd

def init_session_state():
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'show_result' not in st.session_state:
        st.session_state.show_result = False

def reset_quiz():
    st.session_state.step = 0
    st.session_state.answers = {}
    st.session_state.show_result = False

# Definição das questões
questions = [
    {
        'id': 'experience',
        'question': 'Qual sua experiência com café?',
        'info': 'Sua experiência ajuda a determinar recomendações mais adequadas ao seu nível de conhecimento.',
        'options': [
            ('iniciante', 'Iniciante - Estou começando a explorar cafés especiais'),
            ('intermediario', 'Intermediário - Já conheço diferentes tipos de café'),
            ('experiente', 'Experiente - Tenho bastante conhecimento sobre café')
        ]
    },
    {
        'id': 'preparation',
        'question': 'Como você costuma preparar seu café?',
        'info': 'O método de preparo influencia diretamente na extração dos sabores do café.',
        'options': [
            ('coador', 'Coador/Filtro de papel'),
            ('espresso', 'Máquina de Espresso'),
            ('prensa', 'Prensa Francesa'),
            ('hario', 'Hario V60 ou outros métodos filtrados'),
            ('capsulas', 'Máquina de Cápsulas')
        ]
    },
    {
        'id': 'intensity',
        'question': 'Qual intensidade de café você prefere?',
        'info': 'A intensidade está relacionada à concentração e força do sabor do café.',
        'options': [
            ('suave', 'Suave - Sabor delicado e equilibrado'),
            ('medio', 'Médio - Sabor marcante mas não muito forte'),
            ('forte', 'Forte - Sabor intenso e encorpado')
        ]
    },
    {
        'id': 'acidity',
        'question': 'Como você se sente em relação à acidez no café?',
        'info': 'A acidez no café pode ser agradável, lembrando frutas cítricas ou maçã.',
        'options': [
            ('baixa', 'Prefiro café com pouca acidez'),
            ('media', 'Acidez moderada é agradável'),
            ('alta', 'Gosto de notas cítricas e frutadas')
        ]
    },
    {
        'id': 'body',
        'question': 'Qual tipo de corpo (textura) você prefere?',
        'info': 'O corpo é a sensação física do café na boca, sua "densidade".',
        'options': [
            ('leve', 'Leve - Textura mais fluida, como chá'),
            ('medio', 'Médio - Textura equilibrada'),
            ('encorpado', 'Encorpado - Textura mais densa, aveludada')
        ]
    }
]

# Definição dos perfis
profiles = {
    'tradicional': {
        'name': 'Tradicional',
        'description': 'Você aprecia cafés clássicos e equilibrados, com sabores tradicionais e reconfortantes.',
        'characteristics': [
            'Prefere cafés com torra média',
            'Gosta de acidez moderada',
            'Aprecia notas de chocolate e caramelo'
        ],
        'recommendations': [
            {
                'name': 'Blend Tradicional Sul de Minas',
                'price': 'R$ 35,90/250g',
                'description': 'Blend de cafés do Sul de Minas com torra média, notas de chocolate e caramelo.'
            },
            {
                'name': 'Café Bourbon Amarelo',
                'price': 'R$ 42,90/250g',
                'description': 'Café 100% Bourbon Amarelo com torra média e notas de chocolate ao leite.'
            }
        ],
        'tips': [
            'Ideal para preparos em coador de papel',
            'Temperatura ideal de preparo: 92°C',
            'Moagem média a média-fina'
        ]
    },
    'especial': {
        'name': 'Especial/Gourmet',
        'description': 'Você tem um paladar refinado e gosta de explorar cafés com características únicas.',
        'characteristics': [
            'Aprecia cafés com torra clara',
            'Gosta de alta acidez',
            'Valoriza notas frutadas e florais'
        ],
        'recommendations': [
            {
                'name': 'Geisha Panamenho',
                'price': 'R$ 89,90/250g',
                'description': 'Café raro com notas florais, jasmim e frutas cítricas.'
            },
            {
                'name': 'Etiópia Yirgacheffe',
                'price': 'R$ 69,90/250g',
                'description': 'Café africano com notas de bergamota e flores.'
            }
        ],
        'tips': [
            'Métodos de preparo: Hario V60 ou Chemex',
            'Temperatura ideal de preparo: 94°C',
            'Moagem média-fina'
        ]
    },
    'intenso': {
        'name': 'Intenso',
        'description': 'Você prefere cafés com personalidade marcante e sabores intensos.',
        'characteristics': [
            'Prefere torra escura',
            'Gosta de baixa acidez',
            'Aprecia notas de chocolate amargo e especiarias'
        ],
        'recommendations': [
            {
                'name': 'Blend Italiano',
                'price': 'R$ 45,90/250g',
                'description': 'Blend para espresso com notas de chocolate amargo e especiarias.'
            },
            {
                'name': 'Cerrado Mineiro Extra Forte',
                'price': 'R$ 39,90/250g',
                'description': 'Café com torra escura e corpo intenso.'
            }
        ],
        'tips': [
            'Ideal para espresso ou prensa francesa',
            'Temperatura ideal de preparo: 90°C',
            'Moagem média-grossa para prensa, fina para espresso'
        ]
    }
}

def get_coffee_profile(answers):
    if answers.get('intensity') == 'forte' and answers.get('body') == 'encorpado':
        return profiles['intenso']
    elif answers.get('acidity') == 'alta' and answers.get('experience') == 'experiente':
        return profiles['especial']
    else:
        return profiles['tradicional']

def main():

    init_session_state()

    st.title("☕ Descubra seu Perfil de Café")
    st.write("---")

    if not st.session_state.show_result:
        current_q = questions[st.session_state.step]
        
        # Exibir informação sobre a pergunta
        with st.expander("ℹ️ Saiba mais sobre esta pergunta"):
            st.write(current_q['info'])
        
        st.subheader(current_q['question'])
        
        # Criar radio buttons para as opções
        option_labels = [opt[1] for opt in current_q['options']]
        option_values = [opt[0] for opt in current_q['options']]
        
        choice = st.radio(
            "Escolha uma opção:",
            options=range(len(option_labels)),
            format_func=lambda x: option_labels[x],
            label_visibility="collapsed"
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("Próxima" if st.session_state.step < len(questions)-1 else "Ver Resultado"):
                st.session_state.answers[current_q['id']] = option_values[choice]
                if st.session_state.step < len(questions)-1:
                    st.session_state.step += 1
                else:
                    st.session_state.show_result = True
                st.rerun()

        # Mostrar progresso
        st.progress((st.session_state.step + 1) / len(questions))
        st.caption(f"Pergunta {st.session_state.step + 1} de {len(questions)}")

    else:
        profile = get_coffee_profile(st.session_state.answers)
        
        st.header(f"Seu Perfil de Café é: {profile['name']}")
        st.write("---")
        
        st.subheader("Sobre seu perfil")
        st.write(profile['description'])
        
        cola, colb = st.columns(2)
        with colb:
            st.subheader("Suas preferências")
            for char in profile['characteristics']:
                st.write(f"• {char}")
        with cola:
            st.subheader("Cafés recomendados")
            for rec in profile['recommendations']:
                with st.container():
                    st.markdown(f"**{rec['name']}** - {rec['price']}")
                    st.write(rec['description'])
                    st.write("---")
        
        st.subheader("Dicas de preparo")
        for tip in profile['tips']:
            st.write(f"• {tip}")
            
        if st.button("Refazer Questionário"):
            reset_quiz()
            st.rerun()

main()