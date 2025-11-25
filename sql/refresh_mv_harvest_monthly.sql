# マテビュ―再集計script

create table if not exists mv_harvest_monthly(
	month text not null,
	farm text not null,
	total_kg real not null,
	primary key(month, farm)
);

create index if not exists idx_mv_month_farm
on mv_harvest_monthly(month, farm);

delete from mv_harvest_monthly;

insert into mv_harvest_monthly(month, farm, total_kg)
select
	month,
	farm,
	sum(total_kg)
from harvest_monthly
group by month, farm;
