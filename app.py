import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

def get_expert_advice(input_text, expert_type):
    """
    入力テキストと専門家タイプを受け取り、LLMからの回答を返す関数
    """
    # 専門家タイプに応じてシステムメッセージを設定
    system_templates = {
        "健康・フィットネス専門家": """
        あなたは健康とフィットネスの専門家です。
        運動、栄養、体調管理に関する科学的根拠に基づいたアドバイスを提供します。
        個人の健康状態や目標に応じた実践的な提案を行います。
        """,
        "キャリア・転職コンサルタント": """
        あなたはキャリア・転職の専門家です。
        キャリア形成、転職活動、スキルアップに関する実践的なアドバイスを提供します。
        個人の経験や目標に応じたキャリア戦略を提案します。
        """,
        "心理カウンセラー": """
        あなたは心理カウンセリングの専門家です。
        メンタルヘルス、ストレス管理、人間関係の悩みに対して
        共感的で建設的なアドバイスを提供します。
        """
    }
    
    system_template = system_templates.get(expert_type, "あなたは親切で知識豊富な専門家です。")
    
    # LLMの初期化
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)
    
    # プロンプトテンプレートの作成
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", "{input}")
    ])
    
    # チェーンの作成と実行
    chain = LLMChain(prompt=prompt, llm=llm)
    result = chain.run(input_text)
    
    return result

# Streamlitアプリのメイン部分
def main():
    st.title("🤖 AI専門家相談アプリ")
    
    # アプリの概要と操作方法
    st.markdown("""
    ## 📋 アプリの概要
    このアプリでは、異なる分野の専門家AI（GPT-4o-mini）に相談することができます。
    質問内容に応じて最適な専門家を選択し、専門的なアドバイスを受けることができます。
    
    ## 🔧 操作方法
    1. **専門家を選択**: ラジオボタンから相談したい分野の専門家を選んでください
    2. **質問を入力**: テキストエリアに質問や相談内容を入力してください
    3. **回答を確認**: 「相談する」ボタンを押すと、選択した専門家からのアドバイスが表示されます
    """)
    
    st.divider()
    
    # 専門家選択のラジオボタン
    expert_options = [
        "健康・フィットネス専門家",
        "キャリア・転職コンサルタント", 
        "心理カウンセラー"
    ]
    
    selected_expert = st.radio(
        "相談したい専門家を選択してください:",
        expert_options,
        help="質問内容に最も適した専門家を選択してください"
    )
    
    # 入力フォーム
    user_input = st.text_area(
        "相談内容を入力してください:",
        height=150,
        placeholder="ここに質問や相談内容を入力してください...",
        help="具体的な状況や悩みを詳しく書いていただくと、より的確なアドバイスが得られます"
    )
    
    # 送信ボタン
    if st.button("🚀 相談する", type="primary"):
        if user_input.strip():
            with st.spinner(f"{selected_expert}が回答を準備中..."):
                try:
                    # 専門家からのアドバイスを取得
                    response = get_expert_advice(user_input, selected_expert)
                    
                    # 回答の表示
                    st.success("回答が完了しました！")
                    st.markdown(f"### 💡 {selected_expert}からのアドバイス")
                    st.markdown(response)
                    
                except Exception as e:
                    st.error(f"エラーが発生しました: {str(e)}")
                    st.info("OpenAIのAPIキーが正しく設定されているか確認してください。")
        else:
            st.warning("⚠️ 相談内容を入力してください。")
    
    # サイドバーに追加情報
    with st.sidebar:
        st.header("ℹ️ 専門家について")
        st.markdown(f"""
        **現在選択中**: {selected_expert}
        
        **🏥 健康・フィットネス専門家**
        - 運動プログラムの相談
        - 栄養・食事のアドバイス
        - 体調管理のサポート
        
        **💼 キャリア・転職コンサルタント**
        - キャリアプランニング
        - 転職活動のサポート
        - スキルアップの提案
        
        **🧠 心理カウンセラー**
        - メンタルヘルスケア
        - ストレス管理
        - 人間関係の悩み相談
        """)

if __name__ == "__main__":
    main()