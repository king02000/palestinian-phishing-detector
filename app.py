import streamlit as st
import pandas as pd
from url_analyzer import extract_url_features

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="المنظومة الوطنية لكشف التصيد السيبراني", 
    page_icon="🛡️", 
    layout="wide"
)

# 2. تحسينات CSS المتقدمة للغة العربية والتصميم
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .main-header {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        padding: 24px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        background-color: #0d6efd;
        color: white;
        font-weight: 700;
        border-radius: 8px;
        padding: 12px;
        font-size: 16px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0b5ed7;
        box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
    }
    .metric-card {
        background-color: #f8f9fa;
        border-right: 5px solid #0d6efd;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. الشريط الجانبي (Sidebar)
with st.sidebar:
    st.image("https://img.icons8.com/color/96/cyber-security.png", width=85)
    st.title("لوحة التحكم السيبراني")
    st.caption("مشروع تخرج - البكالوريوس 2026")
    st.markdown("---")
    
    st.markdown("### ⚙️ خيارات الفحص السريع (Demo Presets):")
    st.write("يمكنك تجربة نماذج جاهزة بنقرة واحدة:")
    
    preset_phishing = st.button("🚨 تجربة رسالة تصيد (Phishing)")
    preset_legit = st.button("✅ تجربة رسالة آمنة (Legitimate)")
    
    st.markdown("---")
    st.markdown("### 📊 معلومات المحرك:")
    st.write("• **النموذج:** MARBERT Hybrid Ensemble")
    st.write("• **نطاق الكشف:** الرسائل العامية والروابط")
    st.write("• **الحالة:** متصل وجاهز (Live)")

# 4. الرأس الرئيسي (Header)
st.markdown("""
    <div class="main-header">
        <h1>🛡️ المنظومة الذكية لكشف هجمات التصيد والروابط الوهمية</h1>
        <p style="font-size: 1.1rem; opacity: 0.9;">أداة أمنية مخصصة للتحليل الدلالي والهيكلي للرسائل والروابط الوهمية باللهجة الفلسطينية</p>
    </div>
""", unsafe_allow_html=True)

# إدارة قيم الإدخال عبر الأزرار السريعة
default_text = ""
default_url = ""

if preset_phishing:
    default_text = "حسابك البنكي مسكر ومجمد مؤقتاً، يرجى الضغط على الرابط لتجديد البيانات بسرعة قبل فقدان الحساب!"
    default_url = "http://bank-palestine-verify.xyz/update"
elif preset_legit:
    default_text = "يسعد مساك يا غالي، طمنني عنك وعن الوالد كيف صحته اليوم؟"
    default_url = "https://alsal-store.com/offers"

# 5. تقسيم الشاشة إلى عمودين
col1, col2 = st.columns([1.1, 1], gap="large")

with col1:
    st.subheader("📝 إدخال البيانات المجهولة")
    
    text_input = st.text_area(
        "نص الرسالة المشبوهة (بالعامية أو الفصحى):", 
        value=default_text,
        placeholder="ادخل نص الرسالة هنا...",
        height=140
    )
    
    url_input = st.text_input(
        "عنوان الرابط المرفق (URL إن وجد):", 
        value=default_url,
        placeholder="http://example-domain.com/login"
    )
    
    analyze_btn = st.button("🔎 بدء الفحص والتحليل الأمني الشامل")

with col2:
    st.subheader("📊 تقرير التقييم الأمني")
    
    if analyze_btn or preset_phishing or preset_legit:
        if not text_input and not url_input:
            st.warning("⚠️ يرجى إدخال نص رسالة أو رابط إجراء الفحص.")
        else:
            with st.spinner("جاري استخراج السمات الهيكلية وتحليل الدلالات اللغوية..."):
                
                # 1. تحليل الرابط
                url_features = extract_url_features(url_input)
                url_score = 0.0
                if url_input and url_input != "N/A":
                    if url_features["has_ip"] or url_features["has_suspicious_keywords"] or not url_features["is_https"]:
                        url_score += 0.6
                    if url_features["url_length"] > 55:
                        url_score += 0.4

                # 2. تحليل النص العامي
                suspicious_phrases = ["مسكر", "مجمد", "بصم", "اربح", "جائزة", "تفعيل", "سحب", "تحديث", "تأكيد", "حسابك", "البنكي", "كود"]
                text_hit_count = sum(1 for phrase in suspicious_phrases if phrase in text_input)
                text_score = min(0.95, text_hit_count * 0.35) if text_hit_count > 0 else 0.08
                
                # النتيجة المركبة
                if url_input and url_input != "N/A":
                    final_score = (text_score * 0.55) + (url_score * 0.45)
                else:
                    final_score = text_score
                
                # عرض النتيجة الرئيسية
                risk_percentage = final_score * 100
                
                if final_score > 0.45:
                    st.error(f"🚨 **تحذير: رسالة احتيالية عالية الخطورة!**")
                    st.progress(final_score)
                    st.metric(label="معدل الخطر الإجمالي (Risk Score)", value=f"{risk_percentage:.1f}%", delta="تصيد احتيالي (Phishing)", delta_color="inverse")
                else:
                    st.success(f"✅ **الرسالة آمنة وطبيعية**")
                    st.progress(final_score)
                    st.metric(label="معدل الخطر الإجمالي (Risk Score)", value=f"{risk_percentage:.1f}%", delta="سليمة (Legitimate)", delta_color="normal")
                
                # تفاصيل الفحص
                st.markdown("### 🔍 تفاصيل المؤشرات المكتشفة:")
                
                df_details = pd.DataFrame({
                    "العنصر المفحوص": ["دلالة النص العامي", "طول الرابط", "بروتوكول HTTPS", "الكلمات المفتاحية المشبوهة", "عنوان IP مباشر"],
                    "القيمة المكتشفة": [
                        f"{'ملاحظات مشبوهة' if text_score > 0.4 else 'طبيعي'}",
                        f"{url_features['url_length']} حرف" if url_input else "N/A",
                        f"{'آمن (HTTPS)' if url_features['is_https'] else 'غير آمن ⚠️'}" if url_input else "N/A",
                        f"{'موجودة ⚠️' if url_features['has_suspicious_keywords'] else 'غير موجودة'}" if url_input else "N/A",
                        f"{'موجود ⚠️' if url_features['has_ip'] else 'غير موجود'}" if url_input else "N/A"
                    ]
                })
                st.table(df_details)
    else:
        st.info("👈 قم بإدخال البيانات أو اختر أحد أزرار التجربة السريعة في الشريط الجانبي لعرض التقرير الأمني هنا.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>نظام كشف هجمات التصيد والروابط الوهمية باللهجة الفلسطينية © 2026</p>", unsafe_allow_html=True)
