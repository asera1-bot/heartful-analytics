-- copy_harvest_monthly_from_src.sql
-- src: harvests.db の harvest_monthly → harvests_real.db の harvest_monthly へコピー

ATTACH DATABASE '/home/matsuoka/work-automation/heartful-analytics/data/db/harvests.db' AS src;

-- 受け皿を作り直し（列は src に合わせる）
DROP TABLE IF EXISTS harvest_monthly;

CREATE TABLE harvest_monthly AS
SELECT
  farm,
  crop,
  manager,
  month,
  total_kg
FROM src.harvest_monthly;

DETACH DATABASE src;

