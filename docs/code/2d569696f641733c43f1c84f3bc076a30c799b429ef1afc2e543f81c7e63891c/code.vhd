library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity counter is
    Port ( clk : in STD_LOGIC;
           reset : in STD_LOGIC;
           counter_out : out STD_LOGIC_VECTOR (3 downto 0));
end counter;

architecture Behavioral of counter is
signal counter_up : std_logic_vector(3 downto 0);
begin
process(clk,reset)
begin
    if(reset='1') then
        counter_up <= "0000";
    elsif(rising_edge(clk)) then
        counter_up <= counter_up + 1;
    end if;
end process;
counter_out <= counter_up;
end Behavioral;