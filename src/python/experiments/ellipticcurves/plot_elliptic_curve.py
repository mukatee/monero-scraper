import numpy as np
import matplotlib.pyplot as plt
from scipy import spatial

#https://stackoverflow.com/questions/10818546/finding-index-of-nearest-point-in-numpy-arrays-of-x-and-y-coordinates
#find the closest point to a line in the given set of points
#parameter points list defines points to check
#(min_x, min_y) is the start point of line
#(max_x, max_y) is the end point of line
#n_slices is the number of slices to cut the line into
#returns the point from given ṕoints list to any slice generated for the line
#this is used to find curve point (P3) closest to line from P1 to P2
def closest_point(min_x, min_y, max_x, max_y, points, n_slices):
    cur_x = max_x
    cur_y = max_y
    y_slice = (max_y - min_y) / n_slices
    x_slice = (max_x - min_x) / n_slices
    closest_points = []
    #path is a list of the generated points for the line
    path = []
    #distances is the list of distances of each generated point from the curve
    distances = []
    for x in range(n_slices):
        cur_x -= x_slice
        cur_y -= y_slice
        closest = spatial.KDTree(points).query([cur_x, cur_y])
        #print(f"{cur_x},{cur_y}: {closest}")
        distance, idx = closest
        closest_point = tuple(points[idx])
        closest_points.append(closest_point)
        path.append((cur_x, cur_y))
        distances.append(distance)
    return closest_points, path, distances

#plot a line on the given curve (ćplot)
#idx1 = index on curve segments to pick P1 (line start)
#idx2 = index on curve sgments to pick P2 (line end)
#x_offsetter = how much further to draw the line from P1 and P2 (to have some margin on sides)
#ylim_bounds = put some space on top and bottom if needed, to give space for extra line bounds
#n_slices = how many slices to calculate for the line to look for the overlapping points
def plot_line(cplot, idx1, idx2, x_offsetter, ylim_bounds=None, n_slices=10000):
    #this gets the line segments with coordinates from matplotlib
    #will pick the P1 and P2 from those segments later
    c_coords = cplot.allsegs[0][0]
    cx_coords = cplot.allsegs[0][0][:, 0]
    cy_coords = cplot.allsegs[0][0][:, 1]

    #pick x and y coordinates for P1
    myx1 = c_coords[idx1][0]
    myy1 = c_coords[idx1][1]
    #pick x and y coordinates for P2
    myx2 = c_coords[idx2][0]
    myy2 = c_coords[idx2][1]

    #calculate x and y axis length of line, to split it into n_slices
    x_diff = (myx2 - myx1)
    y_diff = (myy2 - myy1)
    #k is the multiplier to get y from x slice idx
    k = y_diff / x_diff
    max_x = max(cx_coords)
    x_diff2 = max_x - myx2
    max_y = myy2 + x_diff2 * k
    min_x = min(cx_coords)
    x_diff3 = (min_x - myx1)*x_offsetter
    min_x += x_diff3*(x_offsetter-1)
    min_y = myy1 + x_diff3 * k
    axes = plt.axes()
    if ylim_bounds is not None:
        axes.set_ylim(ylim_bounds)
        #plot the line,
    plt.plot((min_x, max_x), (min_y, max_y), '-k', color='red')
    plt.grid()

    #find P3, the one that overlaps the curve at the third point
    closest_points, path, distances = closest_point(min_x, min_y, max_x, max_y, c_coords, n_slices)
    min_indices = np.argpartition(distances, 3)[:3]

    #plot the 3 closest dots on the line, they should be P1, P2, and P3 from the article
    closest_x = [closest_points[x][0] for x in min_indices]
    closest_y = [closest_points[x][1] for x in min_indices]
    plt.plot(closest_x, closest_y, marker='o', color='red', ls='')


#i picked the base plotting code from https://asecuritysite.com/comms/plot06
#thanks!
def curve25519():
    plt.close()
    a = 486662
    b = 1

    y, x = np.ogrid[-200000000:200000000:100j, -500000:500000:100j]
#    z = pow(y, 2) - pow(x, 3) - pow(x,2) * a - x * b
    cplot = plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - pow(x,2) * a - x * b, [0])
    plot_line(cplot, 50, 200, 1)
    plt.savefig("25519_.png")

#and this one is from here: https://asecuritysite.com/comms/plot05?a=0&b=7
def curveSecp256k1():
    plt.close()
    a = 0
    b = 7

    y, x = np.ogrid[-5:5:100j, -5:5:100j]
    z = pow(y, 2) - pow(x, 3) - x * a - b
    cplot = plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - x * a - b, [0])
    #this curve seems to need fewer slices to get the points looking better
    plot_line(cplot, 110, 145, 3, [-5, 5], n_slices=100)
    plt.savefig("Secp256k1_.png")

#basic commitment example from article. just a base point and a multiplier
def basic_commitment_example():
    plt.close()
    a = 486662
    b = 1

    y, x = np.ogrid[-200000000:200000000:100j, -500000:500000:100j]
    z = pow(y, 2) - pow(x, 3) - pow(x,2) * a - x * b
    cplot = plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - pow(x,2) * a - x * b, [0])

    c_coords = cplot.allsegs[0][0]
    cx_coords = cplot.allsegs[0][0][:, 0]
    cy_coords = cplot.allsegs[0][0][:, 1]
    idx1 = 10
    v = 5
    idx2 = idx1 + v
    myx1 = c_coords[idx1][0]
    myy1 = c_coords[idx1][1]
    myx2 = c_coords[idx2][0]
    myy2 = c_coords[idx2][1]
    plt.plot(myx1, myy1, marker='o', color='blue', ls='')
    plt.plot(myx2, myy2, marker='o', color='red', ls='')
    plt.savefig("basic_commitment_example.png")

#commitment with base point, multiplier and blinding factor naively added. also from article.
def blinded_naive_commitment_example():
    plt.close()
    a = 486662
    b = 1

    y, x = np.ogrid[-200000000:200000000:100j, -500000:500000:100j]
    z = pow(y, 2) - pow(x, 3) - pow(x,2) * a - x * b
    cplot = plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - pow(x,2) * a - x * b, [0])

    c_coords = cplot.allsegs[0][0]
    cx_coords = cplot.allsegs[0][0][:, 0]
    cy_coords = cplot.allsegs[0][0][:, 1]
    idx1 = 10
    v = 5
    r = 11
    idx2 = idx1 + r
    idx3 = idx1 + r + v
    myx1 = c_coords[idx1][0]
    myy1 = c_coords[idx1][1]
    myx2 = c_coords[idx2][0]
    myy2 = c_coords[idx2][1]
    myx3 = c_coords[idx3][0]
    myy3 = c_coords[idx3][1]
    plt.plot(myx1, myy1, marker='o', color='blue', ls='')
    plt.plot(myx2, myy2, marker='o', color='green', ls='')
    plt.plot(myx3, myy3, marker='o', color='red', ls='')
    plt.savefig("blinded_commitment_example.png")

#example of a commitment with two base points, one for blinding, one for amount
def blinded_smart_commitment_example():
    plt.close()
    a = 486662
    b = 1

    y, x = np.ogrid[-200000000:200000000:100j, -500000:500000:100j]
    z = pow(y, 2) - pow(x, 3) - pow(x,2) * a - x * b
    cplot = plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - pow(x,2) * a - x * b, [0])

    c_coords = cplot.allsegs[0][0]
    cx_coords = cplot.allsegs[0][0][:, 0]
    cy_coords = cplot.allsegs[0][0][:, 1]
    idx_g = 10
    idx_h = 20
    v = 5
    r = 11
    idx_r = idx_h + r
    idx_v = idx_g + v
#    idx_c = idx_g + idx_r + v
    idx_c = idx_r + v
    x_g = c_coords[idx_g][0]
    y_g = c_coords[idx_g][1]
    x_h = c_coords[idx_h][0]
    y_h = c_coords[idx_h][1]
    x_r = c_coords[idx_r][0]
    y_r = c_coords[idx_r][1]
    x_v = c_coords[idx_v][0]
    y_v = c_coords[idx_v][1]
    x_c = c_coords[idx_c][0]
    y_c = c_coords[idx_c][1]
    plt.plot(x_g, y_g, marker='o', color='blue', ls='')
    plt.plot(x_v, y_v, marker='o', color='purple', ls='')
    plt.plot(x_h, y_h, marker='o', color='dodgerblue', ls='')
    plt.plot(x_r, y_r, marker='o', color='green', ls='')
    plt.plot(x_c, y_c, marker='o', color='red', ls='')
    plt.savefig("blinded_smart_example.png")

#moneroscraper commitment example from the article, calculating only the H (amount)
#it has a wrong name with _g suffix, it should be _h. had it confused at some point
def monero_pedersen_example_g():
    plt.close()
    a = 486662
    b = 1

    y, x = np.ogrid[-200000000:200000000:100j, -500000:500000:100j]
    z = pow(y, 2) - pow(x, 3) - pow(x,2) * a - x * b
    cplot = plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - pow(x,2) * a - x * b, [0])

    c_coords = cplot.allsegs[0][0]
    cx_coords = cplot.allsegs[0][0][:, 0]
    cy_coords = cplot.allsegs[0][0][:, 1]
    idx_g = 10

    txin_v1 = 10
    txin_v2 = 30
    txin_v3 = 10
    idx_i_v1 = idx_g + txin_v1
    idx_i_v2 = idx_i_v1 + txin_v2
    idx_i_v3 = idx_i_v2 + txin_v3

    txout_v1 = 8
    txout_v2 = 40
    txout_fee = 2
    idx_o_v1 = idx_g + txout_v1
    idx_o_v2 = idx_o_v1 + txout_v2
    idx_o_fee = idx_o_v2 + txout_fee

    x_g = c_coords[idx_g][0]
    y_g = c_coords[idx_g][1]
    x_txin_v1 = c_coords[idx_i_v1][0]
    y_txin_v1 = c_coords[idx_i_v1][1]
    x_txin_v2 = c_coords[idx_i_v2][0]
    y_txin_v2 = c_coords[idx_i_v2][1]
    x_txin_v3 = c_coords[idx_i_v3][0]
    y_txin_v3 = c_coords[idx_i_v3][1]

    x_txout_v1 = c_coords[idx_o_v1][0]
    y_txout_v1 = c_coords[idx_o_v1][1]
    x_txout_v2 = c_coords[idx_o_v2][0]
    y_txout_v2 = c_coords[idx_o_v2][1]
    x_txout_fee = c_coords[idx_o_fee][0]
    y_txout_fee = c_coords[idx_o_fee][1]

    plt.plot(x_g, y_g, marker='o', color='blue', ls='')
    plt.plot(x_txin_v1, y_txin_v1, marker='o', color='purple', ls='')
    plt.plot(x_txin_v2, y_txin_v2, marker='o', color='dodgerblue', ls='')
    plt.plot(x_txin_v3, y_txin_v3, marker='o', color='green', ls='')
    plt.savefig("monero_input_commitment_g.png")
    plt.close()

    cplot = plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - pow(x,2) * a - x * b, [0])
    plt.plot(x_g, y_g, marker='o', color='blue', ls='')
    plt.plot(x_txout_v1, y_txout_v1, marker='o', color='purple', ls='')
    plt.plot(x_txout_v2, y_txout_v2, marker='o', color='dodgerblue', ls='')
    plt.plot(x_txout_fee, y_txout_fee, marker='o', color='green', ls='')
    plt.savefig("monero_output_commitment_g.png")

#the moneroscraper example, visualizing only the G (blinding factor) part of the calculation
#it has the wrong _h suffix, had them confused at some point
def monero_pedersen_example_h():
    plt.close()
    a = 486662
    b = 1

    y, x = np.ogrid[-200000000:200000000:100j, -500000:500000:100j]
    z = pow(y, 2) - pow(x, 3) - pow(x,2) * a - x * b
    cplot = plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - pow(x,2) * a - x * b, [0])

    c_coords = cplot.allsegs[0][0]
    cx_coords = cplot.allsegs[0][0][:, 0]
    cy_coords = cplot.allsegs[0][0][:, 1]
    idx_h = 20

    txin_v1 = 14
    txin_v2 = 85
    txin_v3 = 45
    idx_i_v1 = idx_h + txin_v1
    idx_i_v2 = idx_i_v1 + txin_v2
    idx_i_v3 = idx_i_v2 + txin_v3

    txout_v1 = 33
    txout_v2 = 28
    txout_fee = (txin_v1+txin_v2+txin_v3)-(txout_v1+txout_v2)
    idx_o_v1 = idx_h + txout_v1
    idx_o_v2 = idx_o_v1 + txout_v2
    idx_o_fee = idx_o_v2 + txout_fee

    x_g = c_coords[idx_h][0]
    y_g = c_coords[idx_h][1]
    x_txin_v1 = c_coords[idx_i_v1][0]
    y_txin_v1 = c_coords[idx_i_v1][1]
    x_txin_v2 = c_coords[idx_i_v2][0]
    y_txin_v2 = c_coords[idx_i_v2][1]
    x_txin_v3 = c_coords[idx_i_v3][0]
    y_txin_v3 = c_coords[idx_i_v3][1]

    x_txout_v1 = c_coords[idx_o_v1][0]
    y_txout_v1 = c_coords[idx_o_v1][1]
    x_txout_v2 = c_coords[idx_o_v2][0]
    y_txout_v2 = c_coords[idx_o_v2][1]
    x_txout_fee = c_coords[idx_o_fee][0]
    y_txout_fee = c_coords[idx_o_fee][1]

    plt.plot(x_g, y_g, marker='o', color='blue', ls='')
    plt.plot(x_txin_v1, y_txin_v1, marker='o', color='purple', ls='')
    plt.plot(x_txin_v2, y_txin_v2, marker='o', color='dodgerblue', ls='')
    plt.plot(x_txin_v3, y_txin_v3, marker='o', color='green', ls='')
    plt.savefig("monero_input_commitment_h.png")
    plt.close()

    cplot = plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - pow(x,2) * a - x * b, [0])
    plt.plot(x_g, y_g, marker='o', color='blue', ls='')
    plt.plot(x_txout_v1, y_txout_v1, marker='o', color='purple', ls='')
    plt.plot(x_txout_v2, y_txout_v2, marker='o', color='dodgerblue', ls='')
    #plt.plot(x_txout_fee, y_txout_fee, marker='o', color='green', ls='')
    plt.savefig("monero_output_commitment_h_nofee.png")

    plt.plot(x_txout_fee, y_txout_fee, marker='o', color='green', ls='')
    plt.savefig("monero_output_commitment_h_fee.png")

if __name__ == '__main__':
    #create base plots for the two EC curves in the article
#    curve25519()
    curveSecp256k1()

    #Build the simplified ('fake') commitment visualizations from the article, one at a time
#     basic_commitment_example()
#     blinded_naive_commitment_example()
    blinded_smart_commitment_example()
#     monero_pedersen_example_g()
#     monero_pedersen_example_h()

