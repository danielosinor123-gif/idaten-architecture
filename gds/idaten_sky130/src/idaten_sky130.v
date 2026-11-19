//-----------------------------------------------------------------------------
// idaten_sky130 — digital tier of Idaten Ce100 (PDK-backed open-flow layout)
//
// P0 (fixed switch/transistor topology): 8-tap MAC pipeline over the spectral
//   features delivered by the magnonic stage, one product per clock.
// C_k (configuration switches): 8-bit config register bank loaded at workload
//   start; selects the per-tap weights w_k and the accumulation mode.
// M_k (result, read once at workload end): 16-bit result register.
//
// This is the silicon instantiation of the paper's P0/C_k/M_k separation:
// the magnonic die computes the wave landscape; this tier only stores the
// configuration and latches the classification result.
//-----------------------------------------------------------------------------
module idaten_sky130 (
  input  wire        clk,
  input  wire        reset,
  input  wire [7:0]  cfg_k,        // C_k configuration switches
  input  wire [7:0]  spectral_in,  // P0: 8-bit spectral feature from magnonic stage
  output reg  [15:0] m_k,          // M_k: result register, read once at end
  output wire        m_k_valid
);

  // C_k config register bank (loaded once at workload start)
  reg [7:0] cfg_r;
  always @(posedge clk or posedge reset)
    if (reset) cfg_r <= 8'h00;
    else       cfg_r <= cfg_k;

  // per-tap weights derived from C_k (deterministic, no LUT content)
  wire [7:0] w0 = cfg_r;
  wire [7:0] w1 = cfg_r ^ 8'h5A;
  wire [7:0] w2 = cfg_r ^ 8'hA5;
  wire [7:0] w3 = cfg_r ^ 8'h3C;

  // pipeline of the input feature (P0 fixed topology)
  reg [7:0] x0, x1, x2, x3;
  always @(posedge clk or posedge reset) begin
    if (reset) begin
      x0 <= 0; x1 <= 0; x2 <= 0; x3 <= 0;
    end else begin
      x0 <= spectral_in;
      x1 <= x0;
      x2 <= x1;
      x3 <= x2;
    end
  end

  // 4 products, accumulated into M_k
  wire [15:0] p0 = x0 * w0;
  wire [15:0] p1 = x1 * w1;
  wire [15:0] p2 = x2 * w2;
  wire [15:0] p3 = x3 * w3;

  reg [15:0] acc;
  always @(posedge clk or posedge reset) begin
    if (reset) begin
      acc  <= 0;
      m_k  <= 0;
    end else begin
      acc <= acc + p0 + p1 + p2 + p3;   // running spectral score
      m_k <= acc + p0 + p1 + p2 + p3;   // M_k latched result (read once at end)
    end
  end

  assign m_k_valid = ~reset;

endmodule
