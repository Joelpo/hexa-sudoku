/**
 * Required External Modules
 */
const express = require('express')
// const fs = require('fs')
const path = require('path')
const { builtinModules } = require('module')
const  Web3 = require('web3')
const { parse } = require('url')
const {performance} = require('perf_hooks');
const abi = require('./abi/ExecProofAbi').abi
var exec = require('sync-exec');

// Address of smart contract
const contractAddress = '0x6186DF72515Ab027B78204Ef66dEc3F269499764'
const INFURA_ENDPOINT = 'https://rinkeby.infura.io/v3/1f9c639597de4aa7b7570d6d9c421026'
const DEFAULT_SUDOKU = '0xxxxxBA3X68X5XXXXBX9XDXFX0X4XXXXXXXXXFXXXXADX13XX3X7XXXXXCXXXEXDXX3XF8XXCX2XEXXC21XXXXB8XD5XXXX9XX86XXCXXAFXX74X0XX1XAXX4XXXX8DXXX6XXXXXEXXX397FEXXXX97XXXC5X6AXX9AXXXXBXXX8XDC8XXXDXCXXAXXXXFBXXXXXX5XXXXXXXCXXXX7CAXDX6EXXX3X1CX0EXXXD7XXA9XFEX4XX7XFXX5XX0XX'
/**
 * App Variables
 */
const app = express(); 
const port = process.env.PORT || '8081';

/**
 *  App Configuration
 */
// set ejs as view engine
app.set('view engine', 'ejs');

// set public dir
app.use(express.static(path.join(__dirname, 'public')))

// set css / js frontend libraries
app.use('/css', express.static(path.join(__dirname, 'node_modules/bootstrap/dist/css')))
app.use('/js', express.static(path.join(__dirname, 'node_modules/bootstrap/dist/js')))

/**
 * Routes Definitions
 */
 app.get('/solve/:sudoku', (req, res) => {
    const { content } = req.params
    const initialSudoku = req.params.sudoku
    
    if(initialSudoku.length >= 256){
        // Launch solver  
        try {
            const [solvedSudoku, time] = launchSolver(initialSudoku)
            console.log('Solved : ' + solvedSudoku + ' in : ' + time + ' seconds')
        
            // send data to browser
            res.render(__dirname + '/public/index.ejs', {solvedSudoku:solvedSudoku, time:time, initialSudoku:initialSudoku})
        } catch (error) {
            res.send("Url format not supported " + error)
        }
    } else {
        res.send("Url format not supported. Input Length : " + initialSudoku.length)
    }

    // setnTx of proof of execution to blockchain
    if (typeof ACCOUNT_PRIVATE_KEYS  !== 'undefined'){
        sendExecutionProof(time)
    }
 });  
 app.get('/:sudoku?', (req, res) => {
    var sudoku = req.params.sudoku
    if (typeof sudoku == 'undefined'){
        // load a default sudoku string
        sudoku = DEFAULT_SUDOKU
    }
    res.redirect(`/solve/${sudoku}`);
 })

/**
 * Server Activation
 */
 app.listen(port, () => {
     console.log(`App available on http://localhost:${port}`)
});

function launchSolver(sudoku){
    result = exec(`python HexaSudokuSolver/HexaSolver.py ${sudoku}`).stdout

    sol = result.split('\n') // get 2 lines : the result and execution time

    return [sol[0], sol[1]]
}

/// WEB3 Functions
// Sends transaction to configured web3 provider 
async function sendExecutionProof(timeToSolve){
    const web3 = new Web3(new Web3.providers.HttpProvider(INFURA_ENDPOINT))
    const contract = await new web3.eth.Contract(abi, contractAddress);
    // we need to export your private key : export ACCOUNT_PRIVATE_KEYS="0x23784..."
    if(!process.env.ACCOUNT_PRIVATE_KEYS){
        console.error('Export your private key : export ACCOUNT_PRIVATE_KEYS="0x23784..."')
    }
    const account = await web3.eth.accounts.privateKeyToAccount(process.env.ACCOUNT_PRIVATE_KEYS)
    // console.log(account.address)

    // initialize transaction
    const tx = {
        from: account.address,
        to: contractAddress,
        gas: 2000000,
        value: '0x0',
        data: contract.methods.addExecProof(timeToSolve.toString()).encodeABI()
    }

    // sign and send transaction
    web3.eth.accounts.signTransaction(tx, process.env.ACCOUNT_PRIVATE_KEYS).then(signed => {
        var tran = web3.eth.sendSignedTransaction(signed.rawTransaction);
    
        tran.on('confirmation', (confirmationNumber, receipt) => {
            console.log('confirmation: ' + confirmationNumber);
        });
    
        tran.on('transactionHash', hash => {
            console.log('hash');
            console.log(hash);
        });
    
        tran.on('receipt', receipt => {
            console.log('reciept');
            console.log(receipt);
        });
    
        tran.on('error', console.error);
        });
}