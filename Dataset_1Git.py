# IMPORT LIBRARIES

import pandas as pd
import matplotlib.pyplot as plt

# Load Data

df=pd.read_csv(r"C:\Users\LENOVO\OneDrive\Desktop\Python\Inc 5000\Data Set- Inc5000 Company List_2014.csv")

# DATA CLEANING

clean_df = df.drop(columns=['_input', '_num', '_widgetName', '_source', '_resultNumber', '_pageUrl', 'url'])

# Industry analysis

industry_analysis = clean_df['industry'].value_counts().reset_index()
industry_analysis['percentage'] = (industry_analysis['count'] / sum(industry_analysis['count'])) * 100
industry_analysis = industry_analysis.set_index('industry')

industry_analysis['total revenue'] = clean_df.groupby('industry')['revenue'].sum() / 1000000
industry_analysis['avg revenue'] = clean_df.groupby('industry')['revenue'].mean() / 1000000
industry_analysis['median revenue'] = clean_df.groupby('industry')['revenue'].median() / 1000000

# Revenue concentration analysis

computer_hardware = clean_df.loc[clean_df['industry'] == 'Computer Hardware',['company', 'revenue', 'growth', 'workers']].sort_values('revenue', ascending=False)
computer_hardware['percentage'] = (computer_hardware['revenue'] / computer_hardware['revenue'].sum() * 100)

energy = clean_df.loc[clean_df['industry'] == 'Energy',['company', 'revenue', 'growth', 'workers']].sort_values('revenue', ascending=False)
energy['percentage'] = (energy['revenue'] / energy['revenue'].sum() * 100)

computer_hardware['cumulative sum'] = computer_hardware['percentage'].cumsum()
energy['cumulative sum'] = energy['percentage'].cumsum()

print(computer_hardware)
print(energy)

# Industry analysis

industry_analysis = clean_df['industry'].value_counts().reset_index()
industry_analysis['percentage'] = (industry_analysis['count'] / sum(industry_analysis['count']) * 100)

revenue_analysis = clean_df.groupby('industry')['revenue'].sum() / 1000000
revenue_analysis = revenue_analysis.reset_index(name='total revenue')

average_revenue = clean_df.groupby('industry')['revenue'].mean() / 1000000
average_revenue = average_revenue.reset_index(name='avg revenue')

median_revenue = clean_df.groupby('industry')['revenue'].median() / 1000000
median_revenue = median_revenue.reset_index(name='median revenue')

industry_analysis = industry_analysis.merge(revenue_analysis, on='industry')
industry_analysis = industry_analysis.merge(average_revenue, on='industry')
industry_analysis = industry_analysis.merge(median_revenue, on='industry')

worker_analysis = clean_df.groupby('industry')['workers'].sum()
worker_analysis = worker_analysis.reset_index()
worker_analysis['percentage'] = (worker_analysis['workers'] / worker_analysis['workers'].sum() * 100)

revenue_by_industry = clean_df.groupby('industry')['revenue'].sum()
worker_analysis = worker_analysis.merge(revenue_by_industry, on='industry')
worker_analysis['revenue per worker'] = (worker_analysis['revenue'] / worker_analysis['workers'])
worker_analysis = worker_analysis.sort_values('revenue per worker',ascending=False)

growth_analysis = clean_df.groupby('industry')['growth'].median()
growth_analysis = growth_analysis.reset_index()

# Combine industry metrics

industry_metrics = growth_analysis.merge(worker_analysis, on='industry')
industry_metrics = industry_metrics.rename(columns={'percentage': 'worker percentage'})
revenue_metrics = industry_analysis.loc[:,['industry', 'total revenue', 'avg revenue', 'median revenue']]

industry_metrics = industry_metrics.merge(revenue_metrics, on='industry')
industry_metrics = industry_metrics.drop(columns='worker percentage')
industry_metrics = industry_metrics.set_index('industry')

industry_metrics['company'] = clean_df.groupby('industry')['company'].count()
industry_metrics = industry_metrics.reset_index()
industry_metrics['rev mean median'] = (industry_metrics['avg revenue'] / industry_metrics['median revenue'])

# Geographic analysis

geographic_analysis = clean_df.groupby('state_l')[['workers', 'revenue']].sum()
company_count_by_state = clean_df.groupby('state_l')['company'].count()
geographic_analysis = geographic_analysis.merge(company_count_by_state,on='state_l')

geographic_analysis['median growth'] = (clean_df.groupby('state_l')['growth'].median())
geographic_analysis['revenue per worker'] = (geographic_analysis['revenue'] / geographic_analysis['workers'])
geographic_analysis['median revenue'] = (clean_df.groupby('state_l')['revenue'].median())

geographic_analysis['revenue'] = (geographic_analysis['revenue'] / 1000000000)
geographic_analysis = geographic_analysis.sort_values('workers',ascending=False)


# Visualizations

top_states_by_companies = geographic_analysis.sort_values('company',ascending=False).head(5)

plt.figure(figsize=(10, 6))
plt.bar(top_states_by_companies.index,top_states_by_companies['company'])
plt.title("Top 5 States by Companies")
plt.xlabel("State")
plt.ylabel("Companies")
plt.tight_layout()
plt.show()
plt.close()

top_states_by_revenue = geographic_analysis.sort_values('revenue',ascending=False).head(5)

plt.figure(figsize=(10, 6))
plt.bar(top_states_by_revenue.index,top_states_by_revenue['revenue'])
plt.title("Top 5 States by Revenue")
plt.xlabel("State")
plt.ylabel("Revenue ($ billions)")
plt.tight_layout()
plt.show()
plt.close()

top_states_by_workers = geographic_analysis.sort_values('workers',ascending=False).head(5)
plt.figure(figsize=(10, 6))
plt.bar(top_states_by_workers.index,top_states_by_workers['workers'])
plt.title("Top 5 States by Workers")
plt.xlabel("State")
plt.ylabel("Workers")
plt.tight_layout()
plt.show()
plt.close()

top_states_by_growth = geographic_analysis.sort_values('median growth',ascending=False).head(5)
plt.figure(figsize=(10, 6))

plt.bar(top_states_by_growth.index,top_states_by_growth['median growth'])
plt.title("Top 5 States by Median Growth")
plt.xlabel("State")
plt.ylabel("Median Growth (%)")
plt.tight_layout()
plt.show()
plt.close()


top_states_by_revenue_per_worker = geographic_analysis.sort_values('revenue per worker',ascending=False).head(5)
plt.figure(figsize=(10, 6))
plt.bar(top_states_by_revenue_per_worker.index,top_states_by_revenue_per_worker['revenue per worker'])
plt.title("Top 5 States by Revenue per Worker")
plt.xlabel("State")
plt.ylabel("Revenue per Worker")
plt.tight_layout()
plt.show()
plt.close()

top_states_by_median_revenue = geographic_analysis.sort_values('median revenue',ascending=False).head(5)

plt.figure(figsize=(10, 6))
plt.bar(top_states_by_median_revenue.index,top_states_by_median_revenue['median revenue'])
plt.title("Top 5 States by Median Revenue")
plt.xlabel("State")
plt.ylabel("Median Revenue")
plt.tight_layout()
plt.show()
plt.close()

top_industries_by_companies = industry_metrics.sort_values('company',ascending=False).head(5)

plt.figure(figsize=(10, 6))
plt.bar(top_industries_by_companies['industry'],top_industries_by_companies['company'])
plt.title("Top 5 Industries by Number of Companies")
plt.xlabel("Industry")
plt.ylabel("Number of Companies")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
plt.close()


top_industries_by_workers = industry_metrics.sort_values('workers',ascending=False).head(5)

plt.figure(figsize=(10, 6))
plt.bar(top_industries_by_workers['industry'],top_industries_by_workers['workers'])
plt.title("Top 5 Industries by Workforce")
plt.xlabel("Industry")
plt.ylabel("Number of Workers")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
plt.close()

top_industries_by_revenue = industry_metrics.sort_values('total revenue',ascending=False).head(5)

plt.figure(figsize=(10, 6))
plt.bar(top_industries_by_revenue['industry'],top_industries_by_revenue['total revenue'])
plt.title("Top 5 Industries by Total Revenue")
plt.xlabel("Industry")
plt.ylabel("Revenue ($ millions)")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
plt.close()

top_industries_by_growth = industry_metrics.sort_values('growth',ascending=False).head(5)

plt.figure(figsize=(10, 6))
plt.bar(top_industries_by_growth['industry'],top_industries_by_growth['growth'])
plt.title("Top 5 Industries by Median Growth")
plt.xlabel("Industry")
plt.ylabel("Median Growth (%)")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
plt.close()

top_industries_by_revenue_skew = industry_metrics.sort_values('rev mean median',ascending=False).head(5)
plt.figure(figsize=(10, 6))
plt.bar(top_industries_by_revenue_skew['industry'],top_industries_by_revenue_skew['rev mean median'])
plt.title("Top 5 Industries by Mean/Median Revenue Ratio")
plt.xlabel("Industry")
plt.ylabel("Mean / Median Revenue")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
plt.close()