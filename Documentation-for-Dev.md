# Documentation for Developer

## ข้อมูลทั่วไปสำหรับการติดตั้ง
-	พัฒนาด้วย Python 3.10
-	มีการใช้ line-bot-sdk
-	มีการใช้ google-auth
-	มีการใช้ google-cloud-datastore
-	มีการใช้ google-api-python-client
-	มีการใช้ google-auth-oauthlib
-	จำเป็นที่จะต้องเชื่อม Chatbot ของ Line เข้ากับ cloud function โดยผ่านทาง webhook 
-	สามารถใช้ DialogFlow ร่วมกับ cloud function ได้
-	จะต้องมีการ config ค่าจะต้องมีการระบุ content type และ authorization ใน class LineRespond (อ่านเพิ่มเติมในส่วนประกอบของ software หัวข้อย่อย Line)
-	จะต้องมี config ค่าต่าง ๆ ในการเชื่อมต่อกับ database (อ่านเพิ่มเติมในส่วนประกอบของ software หัวข้อย่อย database)

## ส่วนประกอบของ software
1. Controller: เป็นส่วนที่ช่วยเป็น Orchestrator ระหว่างการ interaction ของ user จาก Line และ DialogFlow
        Api_requester : ใช้สำหรับการ request api จาก Line และ DialogFlow โดยภายในประกอบด้วย 
            class requester ที่มี def ต่าง ๆ ดังต่อไปนี้
                def post_dialogflow ใช้สำหรับการส่ง request ไปยัง DialogFlow โดยผ่าน url webhook
                def post_user ใช้สำหรับการส่ง request ไปยัง chat ของ user ผ่านทาง api user
                def get_user ใช้สำหรับการรับ userId ของ user
                def update_user ใช้สำหรับการ update ข้อของคำถามที่ user ทำ
                def delete_user ใช้สำหรับการลบ user

        line: ใช้สำหรับส่งคำสั่งที่ต้องการให้ Line ตอบกลับ user โดยภายในประกอบด้วย
            class LineRespond ที่มี def ต่าง ๆ ดังต่อไปนี้
                def push ใช้เพื่อให้ Line สามารถตอบกลับ user ได้
                def get_profile ใช้สำหรับการเก็บ user id
        หมายเหตุ: จะต้องมีการระบุ content type และ authorization ซึ่งจะต้องระบุไว้ใน def _init_ ของ class LineRespond

        System : ใช้สำหรับการการระบุ path ของไฟล์ Json ที่จะส่งผ่านกันในแต่ละส่วนของโปรแกรม โดยภายในประกอบด้วย
            class configurator ที่มี def ต่าง ๆ ดังต่อไปนี้
                def get ใช้สำหรับการส่งค่า path ที่ต้องการ
                
        main : เป็นส่วนหลักสำหรับการ run function หลักของ controller โดยประกอบด้วยส่วนต่าง ๆ ดังต่อไปนี้
                def handle_message ใช้สำหรับ 3 ส่วนคือ การเก็บข้อมูลของ user เข้าสู่ database เมื่อ user ทำการเพิ่มเพื่อนกับตัวของแชทบอท และ ใช้สำหรับตอบกลับ user ในกรณีที่ user ต้องการทำแบบสอบถามรวมถึงการคำนวนความเหมาะสมของ user กับประเภทของการลงทุน และ การตอบกลับ user ด้วยสติ๊กเกอร์
                def sendAssessment ใช้สำหรับส่งแบบสอบถามให้กับ user
        มี list ของตัวแปรคำถามที่ใช้สำหรับถามuserและคำตอบสำหรับประเภทการลงทุนที่เหมาะสมกับ user คนนั้น ๆ อยู่ภายในส่วนนี้

2. user : เป็นส่วนที่ใช้ในเก็บข้อมูล user สู่ database
        Db: เป็นคำสั่งต่างๆสำหรับการ interact กับ database โดยภายในจะประกอบด้วย
            Class Cloudsql ที่มี def ต่าง ๆ ดังต่อไปนี้
                def __connect ใช้สำหรับเชื่อมต่อกับ database
                def __close_connection ใช้สำหรับตัดการเชื่อมต่อกับ database
                def query ใช้สำหรับการ run query 
                def query_df ใช้สำหรับการ run query และได้ค่า dataframe 
        หมายเหตุ: จะต้องมีการ config การตั้งค่าต่างๆในการเชื่อมกับ database โดยการระบุไว้ใน def __init__ ภายใน class CloudSql

        System : ใช้สำหรับการการระบุ path ของไฟล์ Json ที่จะส่งผ่านกันในแต่ละส่วนของโปรแกรม โดยภายในประกอบด้วย
            class configurator ที่มี def ต่าง ๆ ดังต่อไปนี้
                def get ใช้สำหรับการส่งค่า path ที่ต้องการ

        user: ใช้สำหรับการสร้าง query เพื่อที่จะ เพิ่ม ลด update user ประกอบด้วย
            class User ที่มี def ต่าง ๆ ดังต่อไปนี้
                def user_create ใช้สำหรับการเพิ่ม user ใหม่ใน database
                def user_retrieve ใช้สำหรับการดีง user จากใน database
                def user_update ใช้สำหรับการแก้ไขข้อมูล user นั้น ๆ ใน database
                def user_delete ใช้สำหรับการลบ user ใน database

        main : เป็นส่วนหลักสำหรับการ run function หลักของ user โดยประกอบด้วยส่วนต่าง ๆ ดังต่อไปนี้
                def user เรียกใช้งานเพื่อ เพิ่ม ดึงข้อมูล แก้ไข และ ลบ user 

## หมายเหตุ
-	ในการ config Database ใน google cloud ควร config ให้เหมาะสมกับปริมาณของผู้ที่เข้ามาใช้งาน เพื่อความเหมาะสมทางด้านค่าใช้จ่าย
-	ตัวต้นแบบที่ทางผู้พัฒนาได้ทำขึ้นจะต้องเปิดและปิด database ใน cloud ในช่วงเวลาที่ dev และ ทดลองใช้เท่านั้น
-	ยังมี feature ที่สามารถทำต่อได้อีกเช่น การส่งข้อมูลข่าวสารไปให้กับผู้ใช้งานซึ่งหากต้องการที่จะพัฒนาต่อ จำเป็นที่จะต้องสร้าง database เพิ่มเติมสำหรับการเก็บข้อมูลข่าวสารด้วย
-	sequence diagram ในไฟล์ readme.md เขียนโดยการใช้ Mermaid JS
	


	
