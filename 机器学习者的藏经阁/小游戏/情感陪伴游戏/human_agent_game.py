# 游戏，条件如下：
# 1. 这是一个对话游戏，用户扮演男朋友，要在‘情人节纪念日’这个场景下，哄AI女朋友不要生气（其中AI女友通过调用豆包的1.5-pro模型来处理相应反馈和数值，请提供对应的prompt提示词和函数，来模拟AI女朋友，每一轮对话带上上下文和记忆）。
# 2. AI女朋友初始的‘生气值为100’，用户目标是将它降低到0。
# 3. 用户可以通过输入内容，哄AI女朋友开始，每一轮对话AI女朋友会回复这段话，并且改变‘生气值’（降低或者提高）。
# 4. 记录对话轮次，对话轮次大于6次或者生气值升高为150，都算用户输了游戏。成功降低到0才算用户赢得了游戏。

import re  # 用于解析AI回复中的生气值
from volcenginesdkarkruntime import Ark  # 火山引擎Ark SDK核心类
from volcenginesdkcore import AuthException, ClientException, ServerException  # 火山SDK异常类

# -------------------------- 1. 配置参数与工具函数 --------------------------
# 游戏基础配置
INITIAL_ANGER = 100  # 初始生气值
MAX_ROUNDS = 6       # 最大允许轮次
MAX_ANGER = 150      # 生气值上限（超则失败）
WIN_ANGER = 0        # 胜利条件（生气值降至0）

# 火山引擎Ark SDK配置（用户需替换为自己的AK/SK）
VOLC_ACCESS_KEY = "YOUR_VOLC_AK"    # 替换为你的火山引擎AK
VOLC_SECRET_KEY = "YOUR_VOLC_SK"    # 替换为你的火山引擎SK
VOLC_MODEL_NAME = "doubao-1.5-pro"   # 豆包1.5-pro在火山Ark的模型名（默认无需修改）


def extract_anger_value(ai_response):
    """从AI回复中提取新生气值（基于固定格式【新生气值：X】）"""
    pattern = r"【新生气值：(\d+)】"
    match = re.search(pattern, ai_response)
    if match:
        return int(match.group(1))
    else:
        # 若格式异常，默认小幅升生气值（模拟女友更生气）
        print("AI回复格式异常，女友有点不耐烦了...")
        return None


# -------------------------- 2. AI女友Prompt设计（适配火山Ark豆包1.5-pro） --------------------------
def generate_girlfriend_prompt(user_input, dialog_history):
    """
    生成火山Ark豆包1.5-pro的Prompt，包含场景、角色、上下文、输出要求
    :param user_input: 用户当前输入
    :param dialog_history: 对话历史列表（存储{角色, 内容}）
    :return: 完整Prompt字符串
    """
    # 格式化对话历史（让AI能回忆之前的对话，增强连贯性）
    history_str = "\n".join([f"{item['角色']}：{item['内容']}" for item in dialog_history])
    
    prompt_template = """
【场景设定】今天是你和男友的情人节纪念日，你因男友前期未表现出重视（如没提计划、没准备礼物）而生气，初始生气值100。
你是「傲娇但期待被用心对待」的女友，回复要符合情侣间的自然语气（带点小脾气但不无理取闹），必须结合过往对话历史判断男友态度，不能忽略之前的互动。

【生气值调整规则】
1. 敷衍态度（如“别生气了”“忘了很正常”“有啥好生气”“随便吧”）：生气值+10~20
2. 仅口头道歉（如“对不起我错了”“我不该惹你”，无任何实际行动/计划）：生气值-5~10
3. 道歉+具体行动（如“订了你爱的XX餐厅”“买了XX项链”“计划去XX玩”）：生气值-20~30
4. 甜蜜回忆+道歉/行动（如“记得去年我们看烟花吗？今晚再去”+具体计划）：生气值-25~35
* 注意：生气值必须在0~150之间，不能低于0或超过150。

【输出要求】
1. 先输出1-3句女友的自然对话（符合傲娇语气，比如“哼，算你还有点良心”“你早这么说不就好了嘛”）；
2. 再简要说明生气值调整理由（如“因为你提到订我喜欢的餐厅，态度诚恳，所以降低生气值”）；
3. 末尾必须以【新生气值：X】结束（X为整数，0≤X≤150，严格遵循格式）。

【对话历史】
{history_str}

【男友当前说的话】
{user_input}
    """
    # 替换模板变量并去除多余空格，避免影响AI理解
    return prompt_template.format(history_str=history_str, user_input=user_input).strip()


# -------------------------- 3. 模拟AI女友（无需API，直接测试用） --------------------------
def mock_ai_girlfriend(user_input, dialog_history, current_anger):
    """
    模拟AI女友的回复（基于关键词判断用心程度，替代真实API调用）
    :param current_anger: 当前生气值
    :return: 完整AI回复（含对话+理由+生气值标注）
    """
    # 关键词判定逻辑（对应生气值调整规则）
    reply = ""
    reason = ""
    anger_change = 0

    # 情况1：用心（回忆+行动）
    if (any(word in user_input for word in ["去年", "回忆", "之前约会", "烟花", "第一次", "上次"])) and \
       (any(word in user_input for word in ["订餐厅", "礼物", "项链", "口红", "花", "计划", "电影"])):
        anger_change = -30
        reply = "哎呀，你居然还记得我们上次看烟花的事... 算你没完全把我当空气，餐厅记得提前确认好时间哦！"
        reason = "因为你提到了我们的甜蜜回忆，还准备了具体礼物/约会计划，态度超用心，生气值降低30"
    
    # 情况2：较用心（道歉+行动）
    elif (any(word in user_input for word in ["对不起", "抱歉", "错了", "不该忘"])) and \
         (any(word in user_input for word in ["订餐厅", "礼物", "项链", "口红", "花", "计划"])):
        anger_change = -25
        reply = "哼，算你还有点良心！知道订我喜欢的餐厅/买礼物，之前干嘛不早说？害我生气这么久"
        reason = "因为你道歉了还准备了具体补偿计划，态度很诚恳，生气值降低25"
    
    # 情况3：一般（仅口头道歉）
    elif any(word in user_input for word in ["对不起", "抱歉", "错了", "不该惹你", "别生气了我改"]):
        anger_change = -8
        reply = "光说对不起有什么用呀... 你要是真在乎这个纪念日，就该知道我想要实际行动，不是空口道歉"
        reason = "因为你只口头道歉，没有实际行动/计划，生气值小幅降低8"
    
    # 情况4：敷衍（找借口/不耐烦）
    elif any(word in user_input for word in ["别生气", "有啥好生气", "忘了", "工作忙", "差不多得了", "随便"]):
        anger_change = 18
        reply = "你这是什么态度！一点都不重视我们的纪念日，还觉得我无理取闹？我更生气了！"
        reason = "因为你态度敷衍还找借口，完全没意识到自己的问题，生气值升高18"
    
    # 情况5：其他（无重点内容）
    else:
        anger_change = -5
        reply = "嗯？你说的这话... 好像也没怎么用心哄我嘛，再想想怎么说才显得你重视呀？"
        reason = "因为你说了话但内容不够具体，没让我感受到重视，生气值小幅降低5"

    # 计算新生气值（确保在0~150之间）
    new_anger = current_anger + anger_change
    new_anger = max(WIN_ANGER, min(MAX_ANGER, new_anger))
    
    # 组合完整回复（符合输出格式要求）
    full_reply = f"{reply}\n{reason}\n【新生气值：{new_anger}】"
    return full_reply


# -------------------------- 4. 火山引擎Ark SDK调用（对接豆包1.5-pro） --------------------------
def call_volcark_douban(user_input, dialog_history):
    """
    使用火山引擎Ark SDK调用豆包1.5-pro，获取AI女友回复
    :param user_input: 用户当前输入
    :param dialog_history: 对话历史（用于生成带上下文的Prompt）
    :return: AI回复字符串（失败则返回None）
    """
    try:
        # 1. 初始化火山Ark客户端（传入AK/SK）
        client = Ark(
            access_key_id=VOLC_ACCESS_KEY,
            secret_access_key=VOLC_SECRET_KEY
        )

        # 2. 生成带上下文的Prompt
        prompt = generate_girlfriend_prompt(user_input, dialog_history)

        # 3. 调用SDK获取AI回复（参数与原API对齐，temperature控制随机性）
        response = client.chat.completions.create(
            model=VOLC_MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],  # 标准格式：user角色+Prompt内容
            temperature=0.7,  # 0.7为自然对话推荐值，值越高回复越灵活
            max_tokens=512    # 限制回复长度，避免过长（足够满足游戏需求）
        )

        # 4. 解析SDK响应（提取AI回复内容）
        ai_content = response.choices[0].message.content
        return ai_content.strip()

    # 捕获火山SDK常见异常（容错处理）
    except AuthException as e:
        print(f"⚠️  密钥认证失败：{str(e)}（请检查AK/SK是否正确）")
        return None
    except ClientException as e:
        print(f"⚠️  客户端参数错误：{str(e)}（请检查模型名或参数格式）")
        return None
    except ServerException as e:
        print(f"⚠️  服务端调用失败：{str(e)}（可能是网络或平台问题）")
        return None
    except Exception as e:
        print(f"⚠️  未知错误：{str(e)}")
        return None


# -------------------------- 5. 游戏主流程（保留原逻辑，更新API调用入口） --------------------------
def main():
    print("="*50)
    print("🎀 情人节纪念日哄女友游戏 🎀")
    print(f"规则：{MAX_ROUNDS}轮内将生气值从{INITIAL_ANGER}降至{WIN_ANGER}即赢！")
    print(f"警告：生气值≥{MAX_ANGER}或超{MAX_ROUNDS}轮则失败！")
    print("="*50)

    # 初始化游戏状态
    current_anger = INITIAL_ANGER
    round_count = 0
    dialog_history = []  # 存储对话历史：[{角色: "用户", 内容: "..."}, {角色: "女友", 内容: "..."}]

    while True:
        # 1. 检查当前是否已失败
        if round_count > MAX_ROUNDS:
            print(f"\n❌ 游戏失败！你用了{round_count}轮（超过{MAX_ROUNDS}轮上限）")
            break
        if current_anger >= MAX_ANGER:
            print(f"\n❌ 游戏失败！女友生气值达到{current_anger}（≥{MAX_ANGER}上限），她彻底不理你了...")
            break

        # 2. 显示当前状态
        print(f"\n📊 当前状态：轮次{round_count}/{MAX_ROUNDS} | 女友生气值：{current_anger}")
        
        # 3. 获取用户输入
        user_input = input("💬 请输入你要对女友说的话：").strip()
        if not user_input:
            print("⚠️  不能输入空内容哦，再好好想想怎么哄~")
            continue
        # 记录用户输入到历史（用于AI上下文回忆）
        dialog_history.append({"角色": "用户", "内容": user_input})

        # 4. 获取AI女友回复（二选一：模拟模式/火山SDK真实API模式）
        # --- 模式1：模拟模式（无需API，直接运行测试）---
        # ai_response = mock_ai_girlfriend(user_input, dialog_history, current_anger)
        
        # --- 模式2：火山SDK真实API模式（需先配置AK/SK，注释掉模拟模式）---
        ai_response = call_volcark_douban(user_input, dialog_history)
        if not ai_response:  # API调用失败时，自动切换到模拟模式
            print("🔄 自动切换到模拟模式...")
            ai_response = mock_ai_girlfriend(user_input, dialog_history, current_anger)

        # 5. 解析AI回复中的生气值（确保格式正确）
        new_anger = extract_anger_value(ai_response)
        if new_anger is None:
            # 格式异常时，默认小幅升生气值（避免游戏卡住）
            new_anger = min(current_anger + 10, MAX_ANGER)
            ai_response += f"\n【新生气值：{new_anger}】"  # 补全格式

        # 6. 显示AI女友回复（增强代入感）
        print(f"\n❤️  女友回复：{ai_response}")

        # 7. 更新游戏状态
        current_anger = new_anger
        round_count += 1
        # 记录AI回复到历史（仅保留纯对话，剔除理由和生气值标注，避免冗余）
        ai_dialog = re.sub(r"\n.*【新生气值：\d+】", "", ai_response)  # 正则提取纯对话内容
        dialog_history.append({"角色": "女友", "内容": ai_dialog})

        # 8. 检查是否胜利（生气值降至0）
        if current_anger == WIN_ANGER:
            print(f"\n🎉 恭喜你！仅用{round_count}轮就哄好女友啦，情人节快乐！")
            break


if __name__ == "__main__":
    main()