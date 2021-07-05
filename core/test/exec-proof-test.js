const { expect } = require("chai");

describe("ExecProof", function() {
  it("Should add exec proof and get once added", async function() {
    const ExecProof = await ethers.getContractFactory("ExecProof");
    const execProof = await ExecProof.deploy();
    await execProof.deployed();

    const currentTime = '916108' // secs of execution

    // Add execution proof - seconds of execution
    const addExecProof = await execProof.addExecProof(currentTime);
    // wait until the transaction is mined
    await addExecProof.wait();

    const proof = await execProof.getExecProofs()

    expect(proof[0]).to.equal(currentTime);

    // second try
    const currentTime2 = '9161048948945645495' // secs of execution

    // Add execution proof - seconds of execution
    const addExecProof2 = await execProof.addExecProof(currentTime2);
    // wait until the transaction is mined
    await addExecProof2.wait()

    const proof2 = await execProof.getExecProofs()

    // Assert that both proofs have been stored in contract
    expect(proof2[1]).to.equal(currentTime2)
    expect(proof2[0]).to.equal(currentTime)

  });
});
