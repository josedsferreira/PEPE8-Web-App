from flask import Flask, jsonify, render_template, request, redirect, url_for
from PEPE8 import pepe8

app = Flask(__name__, static_url_path='/static')
pepe8_instance = pepe8()  # Create an instance of the PEPE8 class

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        assembly_code = request.form['assembly_code']

        # Save assembly code to a text file
        with open('assembly_code.txt', 'w') as file:
            file.write(assembly_code)

        # Process the assembly code as needed using the PEPE8 class
        pepe8_instance.loadProgram('assembly_code.txt')

        # Redirect to the processor page
        return redirect(url_for('processor'))

    return render_template('index.html')

@app.route('/processor', methods=['GET','POST'])
def processor():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'clock':
            app.logger.info('Clock button clicked - Calling pepe8_instance.clock()')
            pepe8_instance.clock()
        elif action == 'reset':
            app.logger.info('Reset button clicked - Calling pepe8_instance.reset()')
            pepe8_instance.reset()

    return render_template('processor.html', pepe8=pepe8_instance)

# New route to handle AJAX request for updating variables
@app.route('/run_clock', methods=['POST'])
def run_clock():
    """ app.logger.info('AJAX request to run clock received - Updating variables') """
    pepe8_instance.clock()
    return jsonify(
        PC=pepe8_instance.PC,
        A=pepe8_instance.A,
        SEL_PC=pepe8_instance.SEL_PC,
        SEL_ALU=pepe8_instance.SEL_ALU,
        ESCR_A=pepe8_instance.ESCR_A,
        SEL_A=pepe8_instance.SEL_A,
        SEL_B=pepe8_instance.SEL_B,
        WR=pepe8_instance.WR,
        data = pepe8_instance.data,
        program=pepe8_instance.program
    )

@app.route('/reset_cpu', methods=['POST'])
def reset_cpu():
    """ app.logger.info('AJAX request to reset cpu received - Updating variables') """
    pepe8_instance.reset()
    return jsonify(
        PC=pepe8_instance.PC,
        A=pepe8_instance.A,
        SEL_PC=pepe8_instance.SEL_PC,
        SEL_ALU=pepe8_instance.SEL_ALU,
        ESCR_A=pepe8_instance.ESCR_A,
        SEL_A=pepe8_instance.SEL_A,
        SEL_B=pepe8_instance.SEL_B,
        WR=pepe8_instance.WR,
        data = pepe8_instance.data,
        program=pepe8_instance.program
    )

if __name__ == '__main__':
    app.run(debug=True)
