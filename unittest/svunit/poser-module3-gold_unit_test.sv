`include "svunit_defines.svh"
`include "poser-module3-gold.v"
`include "clk_and_reset.svh"

module module3_unit_test;
  import svunit_pkg::svunit_testcase;

  string name = "module3_ut";
  svunit_testcase svunit_ut;


  //===================================
  // This is the UUT that we're 
  // running the Unit Tests on
  //===================================

  `CLK_RESET_FIXTURE(10,10)

  reg [1:0] bar;
  wire [1:0] foo;
  module3 my_module3(.clk_(clk),
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

  `SVTEST(randGarbage)
    bar = 0;
    repeat (20) begin
      bar = $random();
      pause();
      `FAIL_IF(foo[0] !== bar[0] ^ 1)
      `FAIL_IF(foo[1] !== bar[1] ^ foo[0])
    end
  `SVTEST_END

  `SVUNIT_TESTS_END

endmodule
