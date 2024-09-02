import spiceypy as cspice
import numpy as np
import matplotlib.pyplot as plt


def testray():
    cspice.furnsh("/Users/cmunoz/Juice/juice_spice_kernel/kernels/mk/juice_crema_5_0.tm")
    # '../juice/kernels/mk/juice_crema_4_2b22_1_local.tm')

    et = cspice.utc2et('2030-12-20T00:00:00')
    et = cspice.utc2et('2032-07-03T10:18:23')
    flag = 1
    origin = np.array([1e8, 0, 0])
    ray = np.array([-100, 0, 0])
    while flag == 1:
        xptarr, fndarr = cspice.dskxv(False, 'JUICE_IO_PLASMA_TORUS', [-28968], et, 'JUICE_IPT',
                                      origin, ray)
        if fndarr[0] != 0:
            print([xptarr[0], fndarr[0]])
            origin = xptarr[0] + ray / np.linalg.norm(ray)*1e-6
        flag = fndarr[0]
    return


def testJuice():
    cspice.furnsh("/Users/cmunoz/Juice/juice_spice_kernel/kernels/mk/juice_crema_5_0.tm")

    #et = 992871188.1844599
    #et = cspice.utc2et('2032-12-12T17:04:16')
    #et = cspice.utc2et('2032-09-08T08:00:46')
    #et = cspice.utc2et('2032-09-26T19:39:15')
    et = cspice.utc2et('2032-07-03T10:18:23')
    ABRCORR = 'NONE'
    europa_pos = cspice.spkpos('EUROPA', et, 'JUICE_EPT', ABRCORR, 'JUPITER')[0]
    torus_pos = cspice.spkpos('JUICE_EUROPA_PLASMA_TORUS', et, 'JUICE_EPT', ABRCORR, 'JUPITER')[0]
    juice_pos = cspice.spkpos('JUICE', et, 'JUICE_EPT', ABRCORR, 'JUPITER')[0]
    earth_pos = cspice.spkpos('EARTH', et, 'JUICE_EPT', ABRCORR, 'JUPITER')[0]

    plt.plot([juice_pos[0], earth_pos[0]], [juice_pos[1], earth_pos[1]], color='blue')

    RJ = 69911   # km
    theta = np.linspace(0, 2*np.pi, 180)
    torus_points = []
    for angle in theta:
        torus_points.append([12*RJ*np.cos(angle) + torus_pos[0], 12*RJ*np.sin(angle) + torus_pos[1]])
    for angle in theta:
        torus_points.append([9*RJ*np.cos(angle) + torus_pos[0], 9*RJ*np.sin(angle) + torus_pos[1]])
    torus_points = np.asarray(torus_points)
    plt.plot(torus_points[:, 0], torus_points[:, 1], color='gray')

    flag = 1
    origin = cspice.spkpos('EARTH', et, 'JUICE_EPT', ABRCORR, 'JUICE_EUROPA_PLASMA_TORUS')[0]
    ray = - cspice.spkpos('EARTH', et, 'JUICE_EPT', ABRCORR, 'JUICE')[0]

    sincpt_point = cspice.sincpt('DSK/UNPRIORITIZED', 'JUICE_EUROPA_PLASMA_TORUS',
                                 et, 'JUICE_EPT', ABRCORR, 'JUICE', 'JUICE_EPT', ray)[0] + torus_pos
    plt.scatter(sincpt_point[0], sincpt_point[1], color='gold')

    while flag == 1:
        xptarr, fndarr = cspice.dskxv(False, 'JUICE_EUROPA_PLASMA_TORUS', [-28988], et, 'JUICE_EPT', origin, ray)
        if fndarr[0] != 0:
            print([xptarr[0], fndarr[0]])
            plt.scatter(xptarr[0][0] + torus_pos[0], xptarr[0][1] + torus_pos[1], color='orange', label='xpoint')
            origin = xptarr[0] + ray / np.linalg.norm(ray) * 1e-6
        flag = fndarr[0]

    plt.scatter(europa_pos[0], europa_pos[1], color='blue', label='europa')
    plt.scatter(torus_pos[0], torus_pos[1], color='green', label='torus')
    plt.scatter(juice_pos[0], juice_pos[1], color='red', label='juice')
    plt.scatter(0, 0, color='black', label='jupiter')
    plt.xlim([-1 * 1e7, 1 * 1e7])
    plt.ylim([-1 * 1e7, 1 * 1e7])
    plt.grid()
    plt.legend()
    plt.show()
    return

testJuice()

# 19-JUN-2031 01:32:00 --> et: 992871188.1844599
# srflst = [-28968]
# [1 1 0]:|--> [603171.65644224  26740.43192136 -35385.12446933] 604800.1362998603 2.538433808862134 -3.354127461503592
# sep angle =        0.000002 deg; err target pos = 1475.5186875985614 km
# [1 1 0]:|--> [ 289890.62456811 -240305.46421613  -89066.7626101 ] 386931.7492096742 -39.657107527428316 -13.30809729826876
# sep angle =        0.000003 deg; err target pos = 1723.7838532678907 km
# [1 0 0]:|--> [ 113050.76431271 -391046.66475569 -119368.79941319] 424201.46110259875 -73.87553008949203 -16.34356889064347
# sep angle =        0.000003 deg; err target pos = 1863.9235078332363 km
# [1 1 0]:|--> [ 112084.61781499 -391870.22313792 -119534.35127814] 424751.33250925125 -74.03815490885302 -16.34508989266153
# sep angle =        0.000003 deg; err target pos = 1864.6885514299518 km
# [1 1 0]:|--> [  52650.99253697 -442532.4207025  -129718.47985924] 464148.6339578437 -83.2150389989061 -16.228943050713504
# sep angle =        0.000003 deg; err target pos = 1911.7873076450696 km
# [1 0 0]:|--> [   9850.33100002 -479016.40679434 -137052.50053876] 498334.3605481162 -88.82195504596295 -15.963275957451623
# sep angle =        0.000003 deg; err target pos = 1945.7049419921357 km