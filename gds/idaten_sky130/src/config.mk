export DESIGN_NAME = idaten_sky130
export PLATFORM    = sky130hd

export VERILOG_FILES = $(DESIGN_HOME)/src/$(DESIGN_NICKNAME)/idaten_sky130.v
export SDC_FILE      = $(DESIGN_HOME)/$(PLATFORM)/$(DESIGN_NICKNAME)/constraint.sdc

export ADDER_MAP_FILE :=

export CORE_UTILIZATION = 30
export TNS_END_PERCENT = 100
export SETUP_REPAIR_PHASES = PARALLEL_EVAL
