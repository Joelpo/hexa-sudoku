# Hexadecimal 16x16 Sudoku Solver


This Hexadecimal 16x16 solver uses AI to speed the process of finding a solution. 

![hexadoku solver](https://i.ibb.co/n7PdR6J/Screen-Shot-2021-07-05-at-14-54-21.png)

## Usage

```shell
git clone https://github.com/Joelpo/hexa-sudoku

cd hexa-sudoku/app

yarn install

yarn start 
```

## Send execution proof to smart contract
This step is optional.
Export the private key of an address with some faucet-eth on rinkeby network.

```shell
export ACCOUNT_PRIVATE_KEYS="0x782..."
```

Node backend will send a tx to store an execution proof (containing execution time) in the blockchain every time a puzzle is solved. 
Execution proofs are stored in storage of this smart contract. 
https://rinkeby.etherscan.io/address/0x6186df72515ab027b78204ef66dec3f269499764

## Example hexadoku puzzles

http://localhost:8081/solve/0xxxxxBA3X68X5XXXXBX9XDXFX0X4XXXXXXXXXFXXXXADX13XX3X7XXXXXCXXXEXDXX3XF8XXCX2XEXXC21XXXXB8XD5XXXX9XX86XXCXXAFXX74X0XX1XAXX4XXXX8DXXX6XXXXXEXXX397FEXXXX97XXXC5X6AXX9AXXXXBXXX8XDC8XXXDXCXXAXXXXFBXXXXXX5XXXXXXXCXXXX7CAXDX6EXXX3X1CX0EXXXD7XXA9XFEX4XX7XFXX5XX0XX

http://localhost:8081/solve/x2xxx6xxxxxBxF31xxx6x3xB7xx9xx8x5x4Bx2FxxxxA0xCxxxxFDx59x2xxxxxxxxxxxF6x0xExx2xxxxxDxxxx53FCx4xx6xxxxxx51xxD9xxCx5x314xCxx8xxxxxxxxxx89x4Ax7xDxxxDxxx0xxxE5xxxF4xxxx5xxDx83xxx6xxxxExBxxxxx1x8xxxxFxBxxx87A356xxxxx1xAx3xxxxxxDEA0xxxDExxx2xxxxxxxxxxxx4xxxx29xx

http://localhost:8081/solve/EBxF3xxxx6xxxx4xxC8xxxx5x0xxx6xxx5xxxxxD4ExxxA90xxxx1x4xFxACxxxxx14Bx02C5xEx38AxxAxxxxxB0xx47xxxxx5ExxF1D36B9xxxxxxxx3xxxxxxxE5xxxxxxxxEAxx78x1xxFxD8xx0xxx2xxExBxx7x2xxE9xxxxFxCx6xx9xxxx5xxxxxxxxxEBDx8xF0xxx1xxxxxxxxCxx6xxxDxxx42xxAxxDxE7x5x8xxxxx32x7xxxx6
