from amaranth import *
from amaranth.lib.wiring import Component, In, Out
from amaranth.lib.data import ArrayLayout

class RegisterFile(Component):
    read_addr1:   In(16)  # Address for the first read port
    read_addr2:   In(16)  # Address for the second read port
    write_addr:   In(16)  # Address for the write port
    write_data:   In(32)  # Data to write
    write_enable: In(1)   # Write enable signal

    read_data1:   Out(32)            # Data read from the first port
    read_data2:   Out(32)            # Data read from the second port

    def elaborate(self, platform):
        regs = Array([Signal(32)]*16)
        m = Module()

        # Combinational read logic using Switch and Case
        with m.Switch(self.read_addr1):
            for i in range(16):
                with m.Case(i):
                    m.d.sync += self.read_data1.eq(regs[i])

        with m.Switch(self.read_addr2):
            for i in range(16):
                with m.Case(i):
                    m.d.sync += self.read_data2.eq(regs[i])

        # Synchronous write logic
        with m.If(self.write_enable):
            # Using a multiplexer to determine which register to write to
            with m.Switch(self.write_addr):
                for i in range(16):
                    with m.Case(i):
                        m.d.sync += regs[i].eq(self.write_data)

        return m

if __name__ == "__main__":
    from amaranth.back import verilog
    rf = RegisterFile()
    print(verilog.convert(rf, ports=[rf.read_addr1, rf.read_addr2, rf.write_addr, rf.write_data, 
                                      rf.write_enable, rf.read_data1, rf.read_data2], 
                                      emit_src=False))
