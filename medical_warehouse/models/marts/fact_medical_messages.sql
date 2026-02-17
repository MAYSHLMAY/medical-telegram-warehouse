{{ config(materialized='table') }}

SELECT
    msg_key,
    channel_name,
    content,
    message_timestamp,
    view_count,
    forward_count,
    image_path
FROM {{ ref('stg_telegram_messages') }}
WHERE content IS NOT NULL AND content != ''