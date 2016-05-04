`include "svunit_defines.svh"
`include "poser-module6-gold.v"
`include "clk_and_reset.svh"

module module6_unit_test;
  import svunit_pkg::svunit_testcase;

  string name = "module6_ut";
  svunit_testcase svunit_ut;


  //===================================
  // This is the UUT that we're 
  // running the Unit Tests on
  //===================================

  `CLK_RESET_FIXTURE(10,10)

  reg [1:0] bar;
  wire [1:0] foo;
  module6 my_module6(.clk_(clk),
                     .rst_(rst_n),
                     .bar(bar),
                     .foo(foo));


  //===================================
  // Build
  //===================================
  function void build();
    svunit_ut = new(name);
  endfunction


  //===================================
  // Setup for running the Unit Tests
  //===================================
  task setup();
    svunit_ut.setup();
    /* Place Setup Code Here */
    bar = 0;
    reset();
  endtask


  //===================================
  // Here we deconstruct anything we 
  // need after running the Unit Tests
  //===================================
  task teardown();
    svunit_ut.teardown();
    /* Place Teardown Code Here */

  endtask


  //===================================
  // All tests are defined between the
  // SVUNIT_TESTS_BEGIN/END macros
  //
  // Each individual test must be
  // defined between `SVTEST(_NAME_)
  // `SVTEST_END
  //
  // i.e.
  //   `SVTEST(mytest)
  //     <test code>
  //   `SVTEST_END
  //===================================
  `SVUNIT_TESTS_BEGIN

  `SVTEST(randGarbageLowBit)
    reg [3:0] _foo;
    bar = 0;
    repeat (20) begin
      bar = $random();
      _foo[0] = bar[0] ^ 1;
      _foo[1] = bar[1] ^ _foo[0];
      _foo[2] = bar[0] ^ _foo[1];
      _foo[3] = bar[1] ^ _foo[2];
      pause();
      `FAIL_IF(foo[0] !== _foo[0])
    end
  `SVTEST_END

  `SVTEST(randGarbageHigherBits)
    reg [3:0] _foo;
    reg [2:0] _mux;
    bar = 0;
    repeat (20) begin
      bar = $random();
      _foo[0] = bar[0] ^ 1;
      _foo[1] = bar[1] ^ _foo[0];
      _foo[2] = bar[0] ^ _foo[1];
      _foo[3] = bar[1] ^ _foo[2];
      _mux = _foo[3:1];
      pause();
      if (_mux[1:0] == 3) begin
        `FAIL_IF(foo[1] !== _foo[3])
      end else begin
        `FAIL_IF(foo[1] !== _mux[_mux[1:0]])
      end
    end
  `SVTEST_END

  `SVUNIT_TESTS_END

endmodule
