from linebot import (LineBotApi, WebhookParser)
from linebot.models import (MessageEvent, TextSendMessage, StickerSendMessage, QuickReply, QuickReplyButton, MessageAction)
from system import Configurator
from api_requester import Requester
from line import LineResponse
import json
import datetime

configurator = Configurator("private/config.json")
service_requester = Requester(configurator)
line_bot_api = LineBotApi(configurator.get('line.access_token'))
line_response = LineResponse(configurator.get('line.access_token'))
parser = WebhookParser(configurator.get('line.channel_secret'))

def handle_message(request):
    body = request.get_data(as_text=True)
    print("Request: " + body)
    signature = request.headers['X-Line-Signature']
    events = parser.parse(body, signature)
    for event in events:
        user_id=event.source.user_id
        source = event.source
        if event.type != "unfollow": reply_token = event.reply_token
        if event.type == "unfollow":
            response = service_requester.delete_user(user_id)
        elif event.type == "follow":
            response = service_requester.get_user(user_id)
            user = response.json()
            if user == {}:
                profile = line_response.get_profile(user_id)
                display_name = profile.display_name
                response = service_requester.post_user(event, display_name)
            else: 
                user['status'] = 1
                response = service_requester.update_user(user)
        elif event.type == "message":
            if event.message.type == "text":
                text = event.message.text
                if text in ['1','2','3','4']:
                    response = service_requester.get_user(user_id)
                    data = response.json()
                    question = data['last_question']
                    data['sum_score'] += int(text)
                    data['last_question'] += 1
                    if question <8 : sendAssessment(question, reply_token)
                    else:
                        sum_score = data['sum_score']
                        if sum_score < 11: investment_type = 1
                        elif sum_score <= 16: investment_type = 2
                        elif sum_score <= 22: investment_type = 3
                        elif sum_score <= 28: investment_type = 4
                        else: investment_type = 5       
                        data['sum_score'] = 0
                        data['count_of_assessment'] += 1
                        data['last_question'] = 0
                        data['investment_type'] = investment_type
                        data['finished_assessment_date'] = datetime.date.today().isoformat()
                        reply_text = assessment_result[investment_type-1]
                        line_bot_api.reply_message(reply_token, TextSendMessage(text=reply_text))
                    response = service_requester.update_user(data)
                elif (text == 'แบบทดสอบ'):
                    response = service_requester.get_user(user_id)
                    data = response.json()
                    question = data['last_question']-1
                    sendAssessment(question, reply_token)
                else: service_requester.post_dialogflow(request)
            if event.message.type == "sticker":
                package_id = 11539
                sticker_id = 52114112
                line_bot_api.reply_message(reply_token, StickerSendMessage(package_id,sticker_id))
        else: response = service_requester.post_user(event)

def sendAssessment(question, reply_token):
    reply_text = question_list[question]
    items = []
    for i in range(4):
        items.append(QuickReplyButton(action=MessageAction(type="action", label="("+str(i+1)+")", text=str(i+1))))
    line_bot_api.reply_message(reply_token, TextSendMessage(text=reply_text, quick_reply=QuickReply(items)))

question_list = [
    """มีประสบการณ์เกี่ยวกับการลงทุน มากน้อยแค่ไหนครับ ?
    (1) ไม่มี
    (2) < 1 ปี
    (3) 1 - 5 ปี
    (4) > 5 ปี""",
    """อยากให้ประมาณระยะเวลาที่คาดว่าจะไม่จำเป็นต้องใช้เงินลงทุนที่จะลงทุนส่วนนี้
    (1) < 1 ปี
    (2) 1 - 3 ปี
    (3) 3 - 7 ปี
    (4) > 7 ปี""",
    """KYPST อยากทราบว่าเราต้องการรายได้จากเงินลงทุนส่วนนี้มาใช้เป็นค่าใช้จ่ายประจำหรือเปล่าครับ ?
    (1) ต้องการมากที่สุด
    (2) ต้องการบ้าง
    (3) ต้องการนิดเดียว
    (4) ไม่มีข้อจำกัด อยากได้ผลตอบแทนสูงมาก""",
    """สัดส่วนเงินที่อยากจะลงทุนคิดเป็นเท่าไหร่ของสินทรัพย์ทั้งหมดที่มีครับ ?
    (1) > 60 %
    (2) 30 - 60 %
    (3) 10 - 30%
    (4) < 10%""",
    """ข้อไหนคือทัศนคติที่มีต่อการลงทุน ? 
    (1) ไม่อยากขาดทุนเงินต้นเลย แม้ว่าจะได้ผลตอบแทนสูงขึ้นบ้าง
    (2) ขาดทุนเงินต้นได้นิดนึง เพื่อที่จะได้ผลตอบแทนที่สูงบ้าง
    (3) ขาดทุนเงินต้นได้สบาย เพื่อผลตอบแทนที่สูงกว่า
    (4) ไม่มีข้อจำกัด อยากได้ผลตอบแทนสูงมาก""",
    """เรารับความเสี่ยงได้แค่ไหนนะครับ
    (1) น้อยที่สุด เน้นความปลอดภัยสูง แม้จะได้รับผลตอบแทนต่ำ
    (2) รับได้ระดับหนึ่ง สามารถขาดทุนได้บ้าง เพื่อผลตอบแทนที่สูงขึ้น
    (3) ปานกลาง รับความเสี่ยงได้พอสมควร เพื่อผลตอบแทนที่สูงกว่า
    (4) มาก รับความเสี่ยงได้เต็มที่ เพื่อผลตอบแทนสูงสุด""",
    """ข้อไหนตรงกับตัวเรามากที่สุด ? 
    (1) เงินต้นต้องปลอดภัย แม้ว่าจะได้รับผลตอบแทนแพ้ค่าเงินที่ต่ำลง
    (2) สูญเสียเงินต้นได้บ้าง เพื่อให้ได้ผลตอบแทนสูงกว่าค่าเงินที่ต่ำลง
    (3) เน้นสร้างผลตอบแทนให้สูงกว่าค่าเงินที่ต่ำลงแน่นอน
    (4) ต้องการผลตบแทนให้สูงว่าระดับเงินเฟ้อให้มากที่สุดไปเลย""",
    """เราสามารถขาดทุนจากการลงทุนได้ขนาดไหน ? 
    (1) < 10 %
    (2) 10 - 20 %
    (3) 20 - 50 %
    (4) > 50 %"""
]

assessment_result = [
'''ท่านเป็นผู้ลงทุนประเภท: 
เสี่ยงต่ำ
สินทรัพย์ที่ลงทุนที่เหมาะสม:
ฝากประจำแบบปลอดภาษี
กองทุนสำรองเลี้ยงชีพ
ประกันชีวิต''',
'''ท่านเป็นผู้ลงทุนประเภท:
เสี่ยงปานกลางค่อนไปทางต่ำ
สินทรัพย์ที่ลงทุนที่เหมาะสม:
ตราสารหนี้ภาครัฐ
กองทุนรวมตราสารหนี้''',
'''ท่านเป็นผู้ลงทุนประเภท:
เสี่ยงปานกลางค่อนไปทางสูง
สินทรัพย์ที่ลงทุนที่เหมาะสม:
ตราสารหนี้ภาคเอกชน
กองทุนรวมผสมตราสารหนี้และหุ้นสามัญ
''',
'''ท่านเป็นผู้ลงทุนประเภท: 
เสี่ยงสูง
สินทรัพย์ที่ลงทุนที่เหมาะสม:
กองทุนรวมหุ้น
หุ้นสามัญ''',
'''ท่านเป็นผู้ลงทุนประเภท: 
เสี่ยงสูงมาก
สินทรัพย์ที่ลงทุนที่เหมาะสม:
หุ้นสามัญ
อสังหาริมทรัพย์
ทองคำ
Cryptocurrency
ของสะสม (Brand Name)'''
]