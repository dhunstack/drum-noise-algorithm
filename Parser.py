import json

def to_json_file(curve_param):
    """
    Writes curve parameter to json file.

    Args:
        curve_param (numpy array): Curve parameter.
    """
    with open('curve_param.json', 'w') as outfile:
        json.dump(curve_param, outfile)

def write_params_to_json_file(id, length, osc_freqs, osc_bank_gains, noise_bank_gains, freq_curve_param, noise_curve_param):
    """
    Writes parameters to json file.

    Args:
        params (dict): Parameters.
    """
    with open('Resources/DNA_Synth.json', 'r') as file:
        data = json.load(file)
        data['pattrstorage']['slots'][str(id)]['data']['noise_bank_gains'] = noise_bank_gains
        data['pattrstorage']['slots'][str(id)]['data']['osc_bank_gains'] = osc_bank_gains

        for i in range(len(osc_freqs)):
            data['pattrstorage']['slots'][str(id)]['data']['partial['+str(i+1)+']::A'] = [freq_curve_param[i][0]]
            data['pattrstorage']['slots'][str(id)]['data']['partial['+str(i+1)+']::B'] = [freq_curve_param[i][1]]
            data['pattrstorage']['slots'][str(id)]['data']['partial['+str(i+1)+']::duration'] = [length]
            data['pattrstorage']['slots'][str(id)]['data']['partial['+str(i+1)+']::static_gain'] = [osc_bank_gains[i]]
            data['pattrstorage']['slots'][str(id)]['data']['partial['+str(i+1)+']::osc_freq'] = [osc_freqs[i]]

        for i in range(len(noise_bank_gains)):
            data['pattrstorage']['slots'][str(id)]['data']['partial['+str(i+1)+']::A'] = [noise_curve_param[i][0]]
            data['pattrstorage']['slots'][str(id)]['data']['partial['+str(i+1)+']::B'] = [noise_curve_param[i][1]]
            data['pattrstorage']['slots'][str(id)]['data']['partial['+str(i+1)+']::duration'] = [length]
            data['pattrstorage']['slots'][str(id)]['data']['partial['+str(i+1)+']::static_gain'] = [noise_bank_gains[i]]
        
    ## Read from the JSON file DNASynth.json in Resources folder
    ## Update the values of the parameters
    ## Write the updated values to the same JSON file
    with open('Resources/curve_param.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)


if __name__=="__main__":
    # curve_param = [1,2,3,4]
    # to_json_file(curve_param)
    id = 1
    osc_freqs = [1,2,3,4]
    osc_bank_gains = [1,2,3,4]
    noise_bank_gains = [1,2,3,4,5, 6, 7, 8]
    curve_param = [[1,2,3,4],[5,6,7,8]]
    write_params_to_json_file(id, osc_freqs, osc_bank_gains, noise_bank_gains, curve_param)
