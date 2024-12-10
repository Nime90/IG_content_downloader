def coach_ig_info_gc(handle_name = "monetzamora_"):
  #import data from big query
  from google.colab import auth
  auth.authenticate_user()

  from google.cloud import bigquery
  import pandas as pd

  # Create a BigQuery client
  client = bigquery.Client(project="lenus-ehealth", location="europe-north1" )

  # Construct the query
  query = f"""
  with coach_handle as (
      SELECT distinct 
      customer_profile_id, 
      handle
      FROM `bi-lenus-prod.dbt_datamart.sprout_social_daily` 
  ),
  IG_info as (
      SELECT _date,
      customer_profile_id,
      metrics.lifetime_video_views,
      metrics.lifetime_reactions,
      metrics.lifetime_likes,
      metrics.lifetime_shares_count,
      metrics.lifetime_comments_count,
      perma_link,
      text
      FROM `bi-lenus-prod.sprout_social.posts` 
      where perma_link like '%instagram%' and (perma_link like '%/reel/%' or perma_link like '%/p/%')  
      and customer_profile_id = cast(
          (select distinct ssd.customer_profile_id  
          FROM `bi-lenus-prod.dbt_datamart.sprout_social_daily` ssd 
          where ssd.handle = '{handle_name}' 
          ) as string
      )
  )
  select 
      _date,
      handle,
      lifetime_video_views,
      lifetime_reactions,
      lifetime_likes,
      lifetime_shares_count,
      lifetime_comments_count,
      perma_link,
      text
  from IG_info 
  left join coach_handle
  on cast(IG_info.customer_profile_id as string) = cast(coach_handle.customer_profile_id as string)
  order by _date desc
  """

  # Execute the query and convert the results to a pandas DataFrame
  query_job = client.query(query)
  df = query_job.to_dataframe()
  return df

def coach_ig_info(handle_name = "monetzamora_"):
    from google.cloud import bigquery
    import pandas as pd

    # Initialize a client with the specified project ID
    client = bigquery.Client(project="lenus-ehealth", location="europe-north1" )
  # Construct the query
    query = f"""
    with coach_handle as (
        SELECT distinct 
        customer_profile_id, 
        handle
        FROM `bi-lenus-prod.dbt_datamart.sprout_social_daily` 
    ),
    IG_info as (
        SELECT _date,
        customer_profile_id,
        metrics.lifetime_video_views,
        metrics.lifetime_reactions,
        metrics.lifetime_likes,
        metrics.lifetime_shares_count,
        metrics.lifetime_comments_count,
        perma_link,
        text
        FROM `bi-lenus-prod.sprout_social.posts` 
        where perma_link like '%instagram%' and (perma_link like '%/reel/%' or perma_link like '%/p/%')  
        and customer_profile_id = cast(
            (select distinct ssd.customer_profile_id  
            FROM `bi-lenus-prod.dbt_datamart.sprout_social_daily` ssd 
            where ssd.handle = '{handle_name}' 
            ) as string
        )
    )
    select 
        _date,
        handle,
        lifetime_video_views,
        lifetime_reactions,
        lifetime_likes,
        lifetime_shares_count,
        lifetime_comments_count,
        perma_link,
        text
    from IG_info 
    left join coach_handle
    on cast(IG_info.customer_profile_id as string) = cast(coach_handle.customer_profile_id as string)
    order by _date desc
    """
    # Run the query
    query_job = client.query(query)

    # Fetch the results
    df = query_job.to_dataframe()
    return df

def coach_handles_all(market='Denmark'):
    try:
        from google.colab import auth
        auth.authenticate_user()
    except:
        pass

    from google.cloud import bigquery
    import pandas as pd

    # Initialize a client with the specified project ID
    client = bigquery.Client(project="lenus-ehealth", location="europe-north1")
    # Construct the query
    query = f"""
        SELECT distinct 
        handle
        FROM `bi-lenus-prod.dbt_datamart.sprout_social_daily` 
        where kam_country = '{market}'
        """
    # Run the query
    query_job = client.query(query)

    # Fetch the results
    df = query_job.to_dataframe()
    return df
