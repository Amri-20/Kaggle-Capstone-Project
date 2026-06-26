import os
import matplotlib
matplotlib.use('Agg') # Thread-safe non-interactive backend for matplotlib
import matplotlib.pyplot as plt
import numpy as np

def market_research(topic: str) -> dict:
    """Analyze market, competitors, and trends for a given topic."""
    # A reusable business market research simulation
    topic_clean = topic.strip().lower()
    
    # Mock data depending on keywords
    is_tech = any(k in topic_clean for k in ["tech", "software", "ai", "app", "digital", "saas", "cloud"])
    is_retail = any(k in topic_clean for k in ["store", "retail", "shop", "fashion", "clothes", "food", "restaurant"])
    
    if is_tech:
        competitors = ["BigTech Corp", "FastSaaS Inc", "ScaleAI Systems"]
        trends = ["Increasing AI adoption", "Strict data privacy compliance (GDPR/CCPA)", "Cloud-native modernization"]
        swot = {
            "strengths": ["High scalability", "Low operational overhead", "Fast deployment cycles"],
            "weaknesses": ["Data security risks", "High initial engineering cost", "High talent acquisition cost"],
            "opportunities": ["Global expansion via cloud", "Enterprise integration partnerships", "Automation efficiency gains"],
            "threats": ["Rapid technology obsolescence", "Intense startup competition", "Regulatory compliance tightening"]
        }
    elif is_retail:
        competitors = ["SuperMart global", "LocalBrands Co", "E-Buy Express"]
        trends = ["D2C e-commerce growth", "Personalized customer loyalty programs", "Sustainable sourcing demand"]
        swot = {
            "strengths": ["Direct customer touchpoint", "Immediate cash flows", "Tangible brand presence"],
            "weaknesses": ["Inventory management complexity", "High physical lease costs", "Low net profit margins"],
            "opportunities": ["Omnichannel digital integration", "Subscription boxes/loyalty programs", "Local community branding"],
            "threats": ["Supply chain disruptions", "Inflationary pressure on overheads", "Shift in consumer spending"]
        }
    else:
        competitors = ["Incumbent Leaders", "Mid-market Challengers", "Niche Players"]
        trends = ["Digitalization of processes", "Resource efficiency", "Customer experience focus"]
        swot = {
            "strengths": ["Clear value proposition", "Domain expertise", "Niche market positioning"],
            "weaknesses": ["Limited initial brand awareness", "Capital constraints", "Process inefficiencies"],
            "opportunities": ["Strategic alliance building", "Unmet customer needs in secondary tier", "Tech enablement"],
            "threats": ["Economic downturn risk", "Competitor price cutting", "Shifting customer preferences"]
        }
        
    return {
        "topic": topic,
        "market_trends": trends,
        "competitors": competitors,
        "swot": swot
    }

def calculate_financial_kpis(budget: float, rev_y1: float, rev_y2: float, rev_y3: float) -> dict:
    """Calculate ROI, payback period, net revenue, and financial risk score."""
    total_revenue = rev_y1 + rev_y2 + rev_y3
    net_profit = total_revenue - budget
    roi_percent = (net_profit / budget) * 100 if budget > 0 else 0.0
    
    # Estimate break-even
    payback_years = 0.0
    accumulated = 0.0
    for yr, rev in enumerate([rev_y1, rev_y2, rev_y3], 1):
        accumulated += rev
        if accumulated >= budget and payback_years == 0.0:
            # Linear interpolation
            previous_accumulated = accumulated - rev
            needed = budget - previous_accumulated
            payback_years = (yr - 1) + (needed / rev if rev > 0 else 0)
            
    if payback_years == 0.0:
        payback_years = 3.0 if accumulated > 0 else 99.0 # does not break even in 3 years
        
    # Financial risk score: 1 (low) to 10 (high)
    risk_score = 5
    if roi_percent < 20:
        risk_score += 3
    elif roi_percent > 100:
        risk_score -= 2
        
    if payback_years > 2.5:
        risk_score += 2
    elif payback_years < 1.5:
        risk_score -= 1
        
    risk_score = max(1, min(10, risk_score))
    
    return {
        "budget": f"${budget:,.2f}",
        "estimated_revenue": f"${total_revenue:,.2f}",
        "roi_3yr": f"{roi_percent:.2f}%",
        "net_profit": f"${net_profit:,.2f}",
        "payback_period": f"{payback_years:.1f} years",
        "financial_risk_score": risk_score,
        "cost_details": f"Initial implementation cap-ex: ${budget:,.2f}. 3-Year revenue target: ${total_revenue:,.2f}."
    }

def generate_financial_chart(rev_y1: float, rev_y2: float, rev_y3: float, budget: float, filepath: str) -> str:
    """Generate and save a bar chart comparing budget to projected revenues."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        categories = ['Budget', 'Year 1 Revenue', 'Year 2 Revenue', 'Year 3 Revenue']
        values = [budget, rev_y1, rev_y2, rev_y3]
        
        plt.figure(figsize=(7, 4))
        colors = ['#EF4444', '#10B981', '#059669', '#047857'] # Red for budget, greens for revenues
        
        bars = plt.bar(categories, values, color=colors, width=0.6)
        plt.title('Investment vs. Projected Revenues', fontsize=12, fontweight='bold', pad=15)
        plt.ylabel('Amount ($)', fontsize=10)
        
        # Add labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, height, f'${height:,.0f}', ha='center', va='bottom', fontsize=9)
            
        plt.tight_layout()
        plt.savefig(filepath, dpi=150)
        plt.close()
        return filepath
    except Exception as e:
        return f"Error creating chart: {str(e)}"

def summarize_text(text: str, max_sentences: int = 4) -> str:
    """Extract a high-level summary of raw text."""
    if not text:
        return "No text provided."
    # A simple sentence tokenizer
    sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
    if len(sentences) <= max_sentences:
        return text
    return ". ".join(sentences[:max_sentences]) + "."

def extract_citations(text: str, source_documents: list) -> list:
    """Find references in text and match them to loaded documents."""
    citations = []
    text_lower = text.lower()
    for doc in source_documents:
        doc_name = doc.get("name", "")
        keywords = doc.get("keywords", [])
        
        # Check if doc name or keywords appear in text
        matched = False
        if doc_name.lower() in text_lower:
            matched = True
        else:
            for kw in keywords:
                if kw.lower() in text_lower:
                    matched = True
                    break
                    
        if matched:
            citations.append({
                "source": doc_name,
                "relevance": "Direct content overlap",
                "snippet": doc.get("snippet", "")[:100] + "..."
            })
    return citations
