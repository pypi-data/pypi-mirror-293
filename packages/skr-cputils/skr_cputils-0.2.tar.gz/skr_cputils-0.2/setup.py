from setuptools import setup, find_packages

setup(
		name="skr_cputils",
		version="0.2",
		packages=find_packages(),
		author="Saravana Kumar Rajiah",
		description="Utility libraries to accelerate development. 1) TraverseNestedList - A simple module to traverse and print nested list elements",
		entry_points={
			"console_scripts":[
				"pplist=skr_cputils:print_lol",
			]
		},
)
	