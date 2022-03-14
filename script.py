import pandas as pd #type: ignore

ad_clicks = pd.read_csv('ad_clicks.csv')

# Examine the first few rows of the dataframe
print(ad_clicks.head(10))

# Which utm_source recieved the most traffic for the Shoefly website
utm_traffic = ad_clicks.groupby('utm_source').user_id.count().reset_index()
print(utm_traffic)

# Create a new column in the datafram that indicates whether the ad was actually clicked
ad_clicks['is_click'] = ~ad_clicks.ad_click_timestamp.isnull()
print(ad_clicks.head(10)) # Displays newly added 'is_click' column

# Find the percent of is_click from each utm_source
clicks_by_source = ad_clicks.groupby(['utm_source', 'is_click']).user_id.count().reset_index()
#print(clicks_by_source) # Original dataframe no longer necessary after creating Pivot Table

# Pivot the clicks_by_source dataframe into a more legible table
clicks_by_source_pivoted = clicks_by_source.pivot(
    columns = 'is_click',
    index = 'utm_source',
    values = 'user_id'
  ).reset_index()

# Percent of clicks from each utm_source
clicks_by_source_pivoted['percent_clicked'] = clicks_by_source_pivoted[True] / (clicks_by_source_pivoted[True] + clicks_by_source_pivoted[False])
print(clicks_by_source_pivoted)

# Analyzing an A/B Test
# Ad A or Ad B?
group_type = ad_clicks.groupby('experimental_group').user_id.count().reset_index()
print(group_type)

# Compare is_click between experimental_group
group_type_click = ad_clicks.groupby(['experimental_group', 'is_click']).user_id.count().reset_index()
print(group_type_click)

# Does the day of the week affect clicks between the two experimental_groups
a_clicks = ad_clicks[ad_clicks.experimental_group == 'A']
b_clicks = ad_clicks[ad_clicks.experimental_group == 'B']

a_clicks_df = a_clicks.groupby(['is_click', 'day']).user_id.count().reset_index()
b_clicks_df = b_clicks.groupby(['is_click', 'day']).user_id.count().reset_index()

a_clicks_df_pivot = a_clicks_df.pivot(
    columns = 'is_click',
    index = 'day',
    values = 'user_id'
  ).reset_index()

a_clicks_df_pivot['percent_clicked'] = a_clicks_df_pivot[True] / (a_clicks_df_pivot[True] + a_clicks_df_pivot[False])

b_clicks_df_pivot = b_clicks_df.pivot(
    columns = 'is_click',
    index = 'day',
    values = 'user_id'
  ).reset_index()

b_clicks_df_pivot['percent_clicked'] = b_clicks_df_pivot[True] / (b_clicks_df_pivot[True] + b_clicks_df_pivot[False])

print(a_clicks_df_pivot)
print(b_clicks_df_pivot)

# Based on the data the more logical choice in ads for the company would be AD Type A which showed better numbers every day of the week except for Tuesday.