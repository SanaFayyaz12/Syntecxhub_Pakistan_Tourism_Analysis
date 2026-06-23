# ============================================================
#   PAKISTAN TOURISM PERFORMANCE DASHBOARD
#   Syntecxhub Data Analysis Internship — Project 1
#   Intern: [Your Name] | Dataset: Pakistan Tourism 2015-2024
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Style ────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor' : '#0d1117',
    'axes.facecolor'   : '#161b22',
    'axes.edgecolor'   : '#30363d',
    'text.color'       : '#e6edf3',
    'axes.labelcolor'  : '#e6edf3',
    'xtick.color'      : '#8b949e',
    'ytick.color'      : '#8b949e',
    'axes.grid'        : True,
    'grid.color'       : '#21262d',
    'grid.linestyle'   : '--',
    'grid.alpha'       : 0.6,
    'font.family'      : 'DejaVu Sans',
})

ACCENT   = '#58a6ff'
GREEN    = '#3fb950'
RED      = '#f85149'
YELLOW   = '#d29922'
PURPLE   = '#bc8cff'
ORANGE   = '#ffa657'
PCOLORS  = [ACCENT, GREEN, YELLOW, PURPLE, ORANGE, RED]

# ── 1. LOAD & CLEAN DATA ─────────────────────────────────────
df = pd.read_csv('pakistan_tourism_dataset.csv')
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df['Total_Tourists'] = df['Domestic_Tourists'] + df['International_Tourists']
df['Revenue_Est_USD'] = df['Total_Tourists'] * df['Average_Cost_USD']

print("=" * 60)
print("   🇵🇰  PAKISTAN TOURISM DASHBOARD — KPIs")
print("=" * 60)

# ── 2. KPIs ──────────────────────────────────────────────────
total_tourists   = df['Total_Tourists'].sum()
total_domestic   = df['Domestic_Tourists'].sum()
total_intl       = df['International_Tourists'].sum()
total_revenue    = df['Revenue_Est_USD'].sum()
avg_popularity   = df['Popularity_Score'].mean()
top_city         = df.loc[df['Popularity_Score'].idxmax(), 'City']
top_province     = df.groupby('Province')['Total_Tourists'].sum().idxmax()
intl_share       = (total_intl / total_tourists) * 100

print(f"  👥 Total Tourists       : {total_tourists:,.0f}")
print(f"  🏠 Domestic Tourists    : {total_domestic:,.0f}")
print(f"  ✈️  International        : {total_intl:,.0f}  ({intl_share:.1f}%)")
print(f"  💰 Estimated Revenue    : ${total_revenue/1e9:.2f}B USD")
print(f"  ⭐ Avg Popularity Score : {avg_popularity:.1f}/100")
print(f"  🏆 Top City             : {top_city}")
print(f"  🗺️  Top Province         : {top_province}")
print("=" * 60)

# ── 3. DASHBOARD FIGURE ──────────────────────────────────────
fig = plt.figure(figsize=(22, 16))
fig.patch.set_facecolor('#0d1117')

fig.text(0.5, 0.97, '🇵🇰  PAKISTAN TOURISM PERFORMANCE DASHBOARD',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color='#e6edf3')
fig.text(0.5, 0.945, 'Syntecxhub Data Analysis Internship  |  Dataset: 2015–2024',
         ha='center', va='top', fontsize=11, color='#8b949e')

# ── KPI Strip ────────────────────────────────────────────────
kpi_data = [
    ('👥 Total Tourists',    f'{total_tourists/1e6:.1f}M'),
    ('🏠 Domestic',          f'{total_domestic/1e6:.1f}M'),
    ('✈️  International',     f'{total_intl/1e3:.0f}K'),
    ('💰 Est. Revenue',      f'${total_revenue/1e9:.2f}B'),
    ('⭐ Avg Score',         f'{avg_popularity:.1f}/100'),
    ('🏆 Top City',          top_city),
]
kax = fig.add_axes([0.01, 0.875, 0.98, 0.065])
kax.set_xlim(0,1); kax.set_ylim(0,1); kax.axis('off')
kax.set_facecolor('#0d1117')
for i,(lbl,val) in enumerate(kpi_data):
    x = 0.01 + i*0.165
    rect = plt.Rectangle((x,0.05),0.155,0.9,
        transform=kax.transAxes,
        facecolor='#161b22', edgecolor=ACCENT,
        linewidth=1.2, clip_on=False)
    kax.add_patch(rect)
    kax.text(x+0.0775, 0.72, lbl, transform=kax.transAxes,
             ha='center', fontsize=8, color='#8b949e')
    kax.text(x+0.0775, 0.28, val, transform=kax.transAxes,
             ha='center', fontsize=13, fontweight='bold', color=ACCENT)

# ── PLOTS (3x3 grid) ─────────────────────────────────────────
gs = fig.add_gridspec(3, 3, left=0.05, right=0.97,
                      top=0.86, bottom=0.05,
                      hspace=0.45, wspace=0.35)

# Plot 1 — Yearly Tourist Trend
ax1 = fig.add_subplot(gs[0,0])
yr = df.groupby('Year')['Total_Tourists'].sum() / 1e6
ax1.plot(yr.index, yr.values, color=ACCENT, lw=2.5,
         marker='o', markersize=6, zorder=3)
ax1.fill_between(yr.index, yr.values, alpha=0.15, color=ACCENT)
ax1.set_title('📅 Yearly Tourist Trend', color='#e6edf3', fontsize=11, pad=8)
ax1.set_ylabel('Tourists (Millions)', color='#8b949e', fontsize=8)
ax1.set_xlabel('Year', color='#8b949e', fontsize=8)
for x,y in zip(yr.index, yr.values):
    ax1.annotate(f'{y:.1f}M', (x,y), textcoords='offset points',
                 xytext=(0,7), ha='center', fontsize=7, color='#8b949e')

# Plot 2 — Province-wise Tourists
ax2 = fig.add_subplot(gs[0,1])
prov = df.groupby('Province')['Total_Tourists'].sum().sort_values()
bars = ax2.barh(prov.index, prov.values/1e6,
                color=PCOLORS[:len(prov)], edgecolor='#30363d', linewidth=0.5)
ax2.set_title('🗺️ Province-wise Total Tourists', color='#e6edf3', fontsize=11, pad=8)
ax2.set_xlabel('Tourists (Millions)', color='#8b949e', fontsize=8)
for b in bars:
    ax2.text(b.get_width()+0.05, b.get_y()+b.get_height()/2,
             f'{b.get_width():.1f}M', va='center', fontsize=7.5, color='#e6edf3')

# Plot 3 — Destination Type Pie
ax3 = fig.add_subplot(gs[0,2])
dest = df.groupby('Destination_Type')['Total_Tourists'].sum()
wedges, texts, autos = ax3.pie(
    dest.values, labels=dest.index, autopct='%1.1f%%',
    colors=PCOLORS[:len(dest)], startangle=90,
    textprops={'color':'#e6edf3','fontsize':8},
    wedgeprops={'edgecolor':'#0d1117','linewidth':1.5})
for a in autos: a.set_color('#0d1117'); a.set_fontsize(7)
ax3.set_title('🏔️ Destination Type Share', color='#e6edf3', fontsize=11, pad=8)

# Plot 4 — Domestic vs International per year
ax4 = fig.add_subplot(gs[1,0])
yr2 = df.groupby('Year')[['Domestic_Tourists','International_Tourists']].sum()/1e6
x = np.arange(len(yr2))
w = 0.35
ax4.bar(x-w/2, yr2['Domestic_Tourists'], w, label='Domestic', color=GREEN, alpha=0.85)
ax4.bar(x+w/2, yr2['International_Tourists'], w, label='International', color=PURPLE, alpha=0.85)
ax4.set_xticks(x); ax4.set_xticklabels(yr2.index, rotation=45, fontsize=7)
ax4.set_title('🏠 Domestic vs ✈️ International', color='#e6edf3', fontsize=11, pad=8)
ax4.set_ylabel('Tourists (M)', color='#8b949e', fontsize=8)
ax4.legend(facecolor='#161b22', labelcolor='#e6edf3', fontsize=8)

# Plot 5 — Top 5 Cities by Popularity
ax5 = fig.add_subplot(gs[1,1])
top5 = df.nlargest(5,'Popularity_Score')[['City','Popularity_Score','Safety_Rating']]
y_pos = np.arange(len(top5))
bars5 = ax5.barh(top5['City'].values, top5['Popularity_Score'].values,
                 color=PCOLORS[:5], edgecolor='#30363d')
ax5.set_xlim(0,105)
ax5.set_title('🏆 Top 5 Cities by Popularity', color='#e6edf3', fontsize=11, pad=8)
ax5.set_xlabel('Popularity Score', color='#8b949e', fontsize=8)
for b,sr in zip(bars5, top5['Safety_Rating'].values):
    ax5.text(b.get_width()+0.5, b.get_y()+b.get_height()/2,
             f'{b.get_width()} | ⭐{sr}', va='center', fontsize=8, color='#e6edf3')

# Plot 6 — Avg Cost by Province
ax6 = fig.add_subplot(gs[1,2])
cost = df.groupby('Province')['Average_Cost_USD'].mean().sort_values(ascending=False)
bars6 = ax6.bar(cost.index, cost.values,
                color=PCOLORS[:len(cost)], edgecolor='#30363d', linewidth=0.5)
ax6.set_title('💰 Avg Cost per Tourist (USD)', color='#e6edf3', fontsize=11, pad=8)
ax6.set_ylabel('USD', color='#8b949e', fontsize=8)
ax6.tick_params(axis='x', rotation=20, labelsize=7)
for b in bars6:
    ax6.text(b.get_x()+b.get_width()/2, b.get_height()+3,
             f'${b.get_height():.0f}', ha='center', fontsize=8, color='#e6edf3')

# Plot 7 — Province x Destination Heatmap
ax7 = fig.add_subplot(gs[2,0])
pivot = df.pivot_table(values='Total_Tourists',
                       index='Province', columns='Destination_Type',
                       aggfunc='sum', fill_value=0) / 1e6
sns.heatmap(pivot, ax=ax7, cmap='YlOrRd', annot=True, fmt='.1f',
            linewidths=0.5, linecolor='#0d1117',
            annot_kws={'size':8, 'color':'black'})
ax7.set_title('🗺️ Province × Destination Heatmap\n(Tourists M)', color='#e6edf3', fontsize=10, pad=8)
ax7.tick_params(colors='#8b949e', labelsize=7)
ax7.set_xlabel(''); ax7.set_ylabel('')

# Plot 8 — Peak Season Distribution
ax8 = fig.add_subplot(gs[2,1])
season = df.groupby('Peak_Season')['Total_Tourists'].sum()
bars8 = ax8.bar(season.index, season.values/1e6,
                color=[GREEN, YELLOW, ORANGE, PURPLE][:len(season)],
                edgecolor='#30363d', linewidth=0.5, width=0.5)
ax8.set_title('🌤️ Peak Season Tourist Volume', color='#e6edf3', fontsize=11, pad=8)
ax8.set_ylabel('Tourists (M)', color='#8b949e', fontsize=8)
for b in bars8:
    ax8.text(b.get_x()+b.get_width()/2, b.get_height()+0.02,
             f'{b.get_height():.1f}M', ha='center', fontsize=9, color='#e6edf3')

# Plot 9 — Safety Rating vs Popularity
ax9 = fig.add_subplot(gs[2,2])
sc = ax9.scatter(df['Safety_Rating'], df['Popularity_Score'],
                 c=df['Average_Cost_USD'], cmap='plasma',
                 s=df['Total_Tourists']/50000,
                 alpha=0.8, edgecolors='#30363d', linewidth=0.5)
for _, row in df.iterrows():
    ax9.annotate(row['City'], (row['Safety_Rating'], row['Popularity_Score']),
                 textcoords='offset points', xytext=(4,3),
                 fontsize=6, color='#8b949e')
cbar = plt.colorbar(sc, ax=ax9)
cbar.set_label('Avg Cost (USD)', color='#8b949e', fontsize=7)
cbar.ax.yaxis.set_tick_params(color='#8b949e', labelsize=7)
ax9.set_title('⭐ Safety Rating vs Popularity\n(bubble=tourists, color=cost)',
              color='#e6edf3', fontsize=10, pad=8)
ax9.set_xlabel('Safety Rating (1-5)', color='#8b949e', fontsize=8)
ax9.set_ylabel('Popularity Score', color='#8b949e', fontsize=8)

# ── Save ─────────────────────────────────────────────────────
out = 'pakistan_tourism_dashboard.png'
plt.savefig(out, dpi=150, bbox_inches='tight',
            facecolor='#0d1117', edgecolor='none')
print(f'\n✅ Dashboard saved!')
plt.close()
