const assert = require("assert");
const { execute_cmd, evaluate_exp } = require("../src/aview.ts.js");
const { waitForAdamsConnection } = require("./utils.js");

suite("execute_cmd", function () {
    var model_name = "";
    var msg = "";
    suiteSetup(async () => {
        await new Promise((resolve, reject) => {
            waitForAdamsConnection(resolve);
        });
        await new Promise((resolve, reject) => {
            evaluate_exp("UNIQUE_NAME_IN_HIERARCHY('.model')", console.log, (result) => {
                model_name = result;
                resolve();
            });
        });

        // Create a new model
        await new Promise((resolve) =>
            execute_cmd(
                `model create model=${model_name}`,
                (msg_) => {
                    console.log(msg_);
                    msg = msg_;
                },
                resolve
            )
        );
    });

    test("should execute the command without error", () => {
        assert(msg.startsWith("Command successful: "));
    });

    test("should create a new model", () => {
        evaluate_exp(`db_exists("${model_name}")`, console.log, (result) => {
            assert.strictEqual(result, 1);
        });
    });
});
