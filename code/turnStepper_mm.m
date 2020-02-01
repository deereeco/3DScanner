% Using this function assumes a GT2 belt with a 20T pulley at each end
function turnStepper_mm(my_dist) %input millimeters

    clearvars a
    
    a = arduino('com4');

    writeDigitalPin(a,'D4',1); %sets direction pin to a988 high = 1dir low = other dir

    i_start = 1;
    i_end = 80 * my_dist;
    my_delay = 1e-4;

    while i_start <= i_end   %start turning motor until limit
        writeDigitalPin(a,'D3',1);
        pause(my_delay);
        writeDigitalPin(a,'D3',0);
        pause(my_delay);
        i_start = i_start+1;
    end

end