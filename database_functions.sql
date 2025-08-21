-- SQL function to efficiently get the exact count of lunarcrush_data records
-- Run this in your Supabase SQL Editor to create the function

CREATE OR REPLACE FUNCTION get_lunarcrush_count()
RETURNS INTEGER AS $$
BEGIN
    RETURN (SELECT COUNT(*) FROM public.lunarcrush_data);
END;
$$ LANGUAGE plpgsql;

-- SQL function to efficiently get all unique coin names
-- Run this in your Supabase SQL Editor to create the function

CREATE OR REPLACE FUNCTION get_unique_coin_names()
RETURNS TABLE(coin_name TEXT) AS $$
BEGIN
  RETURN QUERY
  SELECT DISTINCT t.coin_name
  FROM public.lunarcrush_data AS t
  WHERE t.coin_name IS NOT NULL
  ORDER BY t.coin_name;
END;
$$ LANGUAGE plpgsql;
