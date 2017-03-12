
from app.models import db, Term, Description
from app.bot.rule import Rule, ForceChangeStateException, transition
from app.bot.reply_generator import ListTemplate, ButtonTemplate, GenericTemplate

STATE_NEW = 'new'
STATE_POKEMON_SEARCH = 'STATE_POKEMON_SEARCH'
STATE_POKEMON_SEARCH_OK = 'STATE_POKEMON_SEARCH_OK'
STATE_HANDLE_MORE = 'STATE_HANDLE_MORE'
PAYLOAD_POKEMON_DESCRIPTION = 'PAYLOAD_POKEMON_DESCRIPTION'
PAYLOAD_POKEMON_SEARCH = 'PAYLOAD_POKEMON_SEARCH'
PAYLOAD_RELATED_POKEMON = 'PAYLOAD_RELATED_POKEMON'
PAYLOAD_MORE = 'PAYLOAD_MORE'
PAYLOAD_CANCEL = 'PAYLOAD_CANCEL'
PAYLOAD_CONTINUE_POKEMON = 'PAYLOAD_CONTINUE_POKEMON'
PAYLOAD_POKEMON_INFO = 'PAYLOAD_POKEMON_INFO'



import pickle
import jieba
import jieba.posseg as pseg
jieba.set_dictionary('app/data/dict.txt.big')

from app.data import POKEMON_REVERSE_INDEX, POKEMON_NAMES_MAPPING

from collections import defaultdict

PAYLOAD_POKEMONGO_MENU = "PAYLOAD_POKEMONGO_MENU"
PAYLOAD_POKEMONGO_REPORT = "PAYLOAD_POKEMONGO_REPORT"
PAYLOAD_POKEMONGO_FIND = "PAYLOAD_POKEMONGO_FIND"
STATE_POKEMONGO_MENU = "STATE_POKEMONGO_MENU"



class PokemongoMenuRules(Rule):

    @transition(STATE_NEW, {'NLP_decision': STATE_POKEMONGO_MENU}, STATE_NEW)
    def rule_pokemongo_menu(self, bot, user, msg, **template_params):

        target = msg['quick_reply'].get('target')

        if not target:
            return True
        
        term = Term.query.filter_by(english=target).first()
        reply = ButtonTemplate("你想要對Pokemon做什麼？")


        reply.add_postback_button(title="我要Report一隻Pokemon", payload="%s" % (PAYLOAD_POKEMONGO_REPORT))
        reply.add_postback_button(title="我想找Pokemon", payload="%s" % (PAYLOAD_POKEMONGO_FIND))

        reply = reply.generate()
        
        reply['quick_replies'] = [
            bot.reply_gen.QUICK_REPLY_CANCEL
        ]
        
        bot.bot_send_message(user.id, reply)
        
        return True

