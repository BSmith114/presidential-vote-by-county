with vote as (
	select 
		election
		,fips
		,county
		,state
		,dem
		,rep
		,other
		,total
		,total - lag(total, 1, total) OVER (partition by fips Order by election asc) as tdiff
		,dem - lag(dem, 1, dem) OVER (partition by fips Order by election asc) as ddiff
		,rep - lag(rep, 1, rep) OVER (partition by fips Order by election asc) as rdiff
		,other - lag(other, 1, other) OVER (partition by fips Order by election asc) as odiff
		,(dem::decimal/total::decimal)::decimal(5,3) as dem_percent
		,(rep::decimal/total::decimal)::decimal(5,3) as rep_percent
		,(other::decimal/total::decimal)::decimal(5,3) as oth_percent
		,(dem::decimal/total::decimal)::decimal(5,3) - (rep::decimal/total::decimal)::decimal(5,3) as dem_margin
		,case
			when election = 2000
				then null
			when (dem > rep) = (lag(dem, 1) OVER (partition by fips Order by election asc) >  lag(rep, 1, rep) OVER (partition by fips Order by election asc))
				then 0
			else 1
		end flip
	from vw_pres_vote
)

select 
	election
	,fips
	,county
	,state
	,dem
	,rep
	,other
	,tdiff
	,ddiff
	,odiff
	,dem_percent
	,rep_percent
	,oth_percent
	,dem_percent  - lag(dem_percent, 1) OVER (partition by fips order by election asc) as dem_percent_shift
	,rep_percent  - lag(rep_percent, 1) OVER (partition by fips order by election asc) as rep_percent_shift
	,oth_percent  - lag(oth_percent, 1) OVER (partition by fips order by election asc) as oth_percent_shift
	,dem_margin
	,dem_margin - lag(dem_margin, 1) OVER (partition by fips order by election asc) as dem_margin_shift
	,case 
		when dem_margin > 0 and	flip = 1
			then 'Dem'
		when dem_margin < 0 and flip = 1
			then 'GOP'
	end as flip
from 
	vote 
