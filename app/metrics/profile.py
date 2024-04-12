import pstats

stats = pstats.Stats('./metrics/profiling/filter_profile.prof')

stats.print_stats()