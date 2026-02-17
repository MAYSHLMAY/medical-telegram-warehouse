{{ config(materialized='view') }}

WITH raw_data AS (
    SELECT * FROM {{ source('raw_data', 'telegram_messages') }}
)

SELECT
    id AS msg_key,
    channel_name,
    message_id,
    -- Fix the date format
    CAST(message_date AS TIMESTAMP) AS message_timestamp,
    -- Clean text
    TRIM(message_text) AS content,
    has_media,
    COALESCE(views, 0) AS view_count,
    COALESCE(forwards, 0) AS forward_count,
    image_path
FROM raw_data
WHERE message_text IS NOT NULL OR has_media = True