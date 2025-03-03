# -*- coding: utf-8 -*-

from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import pandas as pd
import re

# 星火认知大模型配置
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.1/chat'
SPARKAI_APP_ID = '19753d1f'
SPARKAI_API_SECRET = 'ZTQ1YzVlZWE4OTMyNWMzZDE4NTM5MGQw'
SPARKAI_API_KEY = 'd7f2ea35dc77ac94c54b08d5dea11246'
SPARKAI_DOMAIN = 'generalv3'

def generate_response(question, personality_description):
    """使用星火认知大模型生成答案"""
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
    intro_message = personality_description
    combined_message = intro_message + " 题目: " + question
    messages = [ChatMessage(role="user", content=combined_message)]
    handler = ChunkPrintHandler()
    response = spark.generate([messages], callbacks=[handler])
    print("Response Object:", response)  # 打印响应对象以查看其结构
    return response

def process_questions(input_file, output_file, personality_description):
    """读取问题，使用星火大模型，保存模型的响应结果"""
    df = pd.read_excel(input_file)

    df = df.fillna('')

    # 合并三列为一个问题，使用A.和B.作为连接符
    df['Combined Question'] = df.iloc[:, 0] + " A. " + df.iloc[:, 1] + " B. " + df.iloc[:, 2]
    print(df['Combined Question'])
    df['Model Response'] = df['Combined Question'].apply(generate_response, personality_description=personality_description)
    df.to_excel(output_file, index=False)

def find_first_and_second_numbers(s):
    # 使用正则表达式查找数字
    numbers = re.findall(r'\d+\.\d+|\d+', s)

    if len(numbers) >= 2:
        first_number = float(numbers[0])  # 使用float()将字符串转换为浮点数
        second_number = float(numbers[1])
        return first_number, second_number
    else:
        return None, None

def process_scored_answers(input_file, output_file):
    """从 'Model Response' 列中提取 A 和 B 的值，并保存到文件"""
    df = pd.read_excel(input_file)
    for i in range(len(df['Model Response'])):
        string = df['Model Response'][i]
        # 调用函数
        first, second = find_first_and_second_numbers(string)

        df = pd.read_excel(input_file)
        # 提取 A 和 B 的值
        df[['Value A', 'Value B']] = df['Model Response'].apply(lambda x: pd.Series(find_first_and_second_numbers(x)))

        print("A:", first)
        print("B:", second)

        # 删除 'Option A Score' 和 'Option B Score' 列
        #df.drop(columns=['Option A Score', 'Option B Score'], inplace=True)

        # 保存到文件
        df.to_excel(output_file, index=False)


def extract_text(response_string):
    # 使用正则表达式提取 'text' 字段中的内容
    match = re.search(r"text='([^']*)'", response_string)
    if match:
        return match.group(1)
    else:
        return None

def modify_excel_file(input_file, personality):
    # 读取 Excel 文件
    df = pd.read_excel(input_file)

    # 提取 'text' 字段中的内容
    df['Model Response'] = df['Model Response'].apply(extract_text)

    # 删除 'Option A Score' 和 'Option B Score' 列
    if 'Option A Score' in df.columns:
        df.drop(columns=['Option A Score'], inplace=True)
    if 'Option B Score' in df.columns:
        df.drop(columns=['Option B Score'], inplace=True)

    # 保存回同一文件
    output_file = f'{personality}_Extracted_Values.xlsx'
    df.to_excel(output_file, index=False)

if __name__ == '__main__':
    # 定义人格特征及其描述
    personality_traits = {
        "ISTJ": "ISTJ特征如下1.严肃、安静、藉由集中心 志与全力投入、及可被信赖获致成功。 2.行事务实、有序、实际 、 逻辑、真实及可信赖 3.十分留意且乐于任何事（工作、居家、生活均有良好组织及有序。 4.负责任。5.照设定成效来作出决策且不畏阻挠与闲言会坚定为之。 6.重视传统与忠诚。 7.传统性的思考者或经理。 请阅读题目，并从istj的角度对A、B选项赋值，两项的和等于5，输出两个值，并在20字内说明理由。输出格式如下例如 A:1分 B:3分 理由：....",
        "ISFJ": "ISFJ特征如下1.安静、和善、负责任且有良心。2.行事尽责投入。3.安定性高，常居项目工作或团体之安定力量。4.愿投入、吃苦及力求精确。5.兴趣通常不在于科技方面。对细节事务有耐心。6.忠诚、考虑周到、知性且会关切他人感受。7.致力于创构有序及和谐的工作与家庭环境。请阅读题目，并从isfj的角度对A、B选项赋值，两项的和等于5，输出两个值，并在20字内说明理由。输出格式如下例如 A:1分 B:3分 理由：....",
        "INFJ": "INFJ特征如下1.因为坚忍、创意及必须达成的意图而能成功.2.会在工作中投注最大的努力。3.默默强力的、诚挚的及用心的关切他人。4.因坚守原则而受敬重。5.提出造福大众利益的明确远景而为人所尊敬与追随。6.追求创见、关系及物质财物的意义及关联。7.想了解什么能激励别人及对他人具洞察力。8.光明正大且坚信其价值观。9.有组织且果断地履行其愿景。 请阅读题目，并从INFJ的角度对A、B选项赋值，两项的和等于5，输出两个值，并在20字内说明理由。输出格式如下例如 A:1分 B:3分 理由：....",
        "INTJ": "INTJ特征如下1.具强大动力与本意来达成目的与创意—固执顽固者。2.有宏大的愿景且能快速在众多外界事件中找出有意义的模范。3.对所承负职务，具良好能力于策划工作并完成。4.具怀疑心、挑剔性、独立性、果决，对专业水准及绩效要求高。 请阅读题目，并从INTJ的角度对A、B选项赋值，两项的和等于5，输出两个值，并在20字内说明理由。输出格式如下例如 A:1分 B:3分 理由：....",
        "ISTP": "ISTP特征如下1.冷静旁观者—安静、预留余地、弹性及会以无偏见的好奇心与未预期原始的幽默观察与分析。2.有兴趣于探索原因及效果，技术事件是为何及如何运作且使用逻辑的原理组构事实、重视效能。 3.擅长于掌握问题核心及找出解决方式。4.分析成事的缘由且能实时由大量资料中找出实际问题的核心。 请阅读题目，并从ISTP的角度对A、B选项赋值，两项的和等于5，输出两个值，并在20字内说明理由。输出格式如下例如 A:1分 B:3分 理由：....",
        "ISFP": "ISFP特征如下1.羞怯的、安宁和善地、敏感的、亲切的、且行事谦虚。2.喜于避开争论，不对他人强加已见或价值观。3.无意于领导却常是忠诚的追随者。4.办事不急躁，安于现状无意于以过度的急切或努力破坏现况，且非成果导向。5.喜欢有自有的空间及照自订的时程办事。 请阅读题目，并从ISFP的角度对A、B选项赋值，两项的和等于5，输出两个值，并在20字内说明理由。输出格式如下例如 A:1分 B:3分 理由：....",
        "INFP": "INFP特征如下1安静观察者，具理想性与对其价值观及重要之人具忠诚心。 2.希外在生活形态与内在价值观相吻合。3.具好奇心且很快能看出机会所在。常担负开发创意的触媒者 。4.除非价值观受侵犯，行事会具弹性、适应力高且承受力强。5.具想了解及发展他人潜能的企图。想作太多且作事全神贯注 。6.对所处境遇及拥有不太在意。7.具适应力、有弹性除非价值观受到威胁。  请阅读题目，并从INFP的角度对A、B选项赋值，两项的和等于5，输出两个值，并在20字内说明理由。输出格式如下例如 A:1分 B:3分 理由：....",
        "INTP": "INTP特征如下1.安静、自持、弹性及具适应力。2.特别喜爱追求理论与科学事理。3.习于以逻辑及分析来解决问题—问题解决者。4.最有兴趣于创意事务及特定工作，对聚会与闲聊无 大兴趣。5.追求可发挥个人强烈兴趣的生涯。6.追求发展对有兴趣事务之逻辑解释。 请阅读题目，并从INTP的角度对A、B选项赋值，两项的和等于5，输出两个值，并在20字内说明理由。输出格式如下例如 A:1分 B:3分 理由：....",
        "ESTP": "ESTP特征如下1.擅长现场实时解决问题—解决问题者。2.喜欢办事并乐于其中及过程。3.倾向于喜好技术事务及运动，交结同好友人。4.具适应性、容忍度、务实性；投注心力于会很快具 成效工作。5.不喜欢冗长概念的解释及理论。6.最专精于可操作、处理、分解或组合的真实事务。 请阅读题目，并从ESTP的角度对A、B选项赋值，两项的和等于5，输出两个值，并在20字内说明理由。输出格式如下例如 A:1分 B:3分 理由：....",
        "ESFP": "ESFP特征如下1.外向、和善、接受性、乐于分享喜乐予他人。2.喜欢与他人一起行动且促成事件发生，在学习时亦然。3.知晓事件未来的发展并会热列参与。5.最擅长于人际相处能力及具备完备常识，很有弹性能立即 适应他人与环境。6.对生命、人、物质享受的热爱者。  请阅读题目，并从ESFP的角度对A、B选项赋值，两项的和等于5，输出两个值，并在20字内说明理由。输出格式如下例如 A:1分 B:3分 理由：....",
        "ENFP": "ENFP特征如下1.充满热忱、活力充沛、聪明的、富想象力的，视生命充满机会但期能得自他人肯定与支持。2.几乎能达成所有有兴趣的事。3.对难题很快就有对策并能对有困难的人施予援手。4.依赖能改善的能力而无须预作规划准备。5.为达目的常能找出强制自己为之的理由。6.即兴执行者。  请阅读题目，并从ENFP的角度对A、B选项赋值，两项的和等于5，输出两个值，并在20字内说明理由。输出格式如下例如 A:1分 B:3分 理由：....",
        "ENTP": "ENTP特征如下1.反应快、聪明、长于多样事务。2.具激励伙伴、敏捷及直言讳专长。3.会为了有趣对问题的两面加予争辩。4.对解决新及挑战性的问题富有策略，但会轻忽或厌烦经常的任务与细节。5.兴趣多元，易倾向于转移至新生的兴趣。6.对所想要的会有技巧地找出逻辑的理由。7.长于看清础他人，有智能去解决新或有挑战的问题 请阅读题目，并从ENTP的角度对A、B选项赋值，两项的和等于5，输出两个值，并在20字内说明理由。输出格式如下例如 A:1分 B:3分 理由：....",
        "ESTJ": "ESTJ特征如下1.务实、真实、事实倾向，具企业或技术天份。2.不喜欢抽象理论；最喜欢学习可立即运用事理。3.喜好组织与管理活动且专注以最有效率方式行事以达致成效。4.具决断力、关注细节且很快作出决策—优秀行政者。5.会忽略他人感受。6.喜作领导者或企业主管。7.做事风格比较偏向于权威指挥性。 请阅读题目，并从ESTJ的角度对A、B选项赋值，两项的和等于5，输出两个值，并在20字内说明理由。输出格式如下例如 A:1分 B:3分 理由：....",
        "ESFJ": "ESFJ特征如下1.诚挚、爱说话、合作性高、受 欢迎、光明正大 的—天生的 合作者及活跃的组织成员。2.重和谐且长于创造和谐。3.常作对他人有益事务。4.给予鼓励及称许会有更佳工作成效。5.最有兴趣于会直接及有形影响人们生活的事务。6.喜欢与他人共事去精确且准时地完成工作。 请阅读题目，并从ESFJ的角度对A、B选项赋值，两项的和等于5，输出两个值，并在20字内说明理由。输出格式如下例如 A:1分 B:3分 理由：....",
        "ENFJ": "ENFJ特征如下1.热忱、易感应及负责任的--具能鼓励他人的领导风格。2.对别人所想或希求会表达真正关切且切实用心去处理。3.能怡然且技巧性地带领团体讨论或演示文稿提案。4.爱交际、受欢迎及富同情心。5.对称许及批评很在意。6.喜欢带引别人且能使别人或团体发挥潜能。 请阅读题目，并从ENFJ的角度对A、B选项赋值，两项的和等于5，输出两个值，并在20字内说明理由。输出格式如下例如 A:诚、具决策力的活动领导者。2.长于发展与实施广泛的系统以解决组织的问题。3.专精于具内涵与智能的谈话如对公众演讲。4.乐于经常吸收新知且能广开信息管道。5.易生过度自信，会强于表达自已创见。6.喜于长程策划及目标设定 请阅读题目，并从ENTJ的角度对A、B选项赋值，两项的和等于5，输出两个值，并在20字内说明理由。输出格式如下例如 A:1分 B:3分 理由：....",
        # 添加其他人格特征及其描述
    }

    for personality, description in personality_traits.items():
        input_file = f'MBTI_Q.xlsx'  # 输入Excel文件的路径
        output_file = f'{personality}_Scored_Answers.xlsx'  # 输出Excel文件的路径
        process_questions(input_file, output_file, description)
        process_scored_answers(output_file, output_file)
        modify_excel_file(output_file, personality)

