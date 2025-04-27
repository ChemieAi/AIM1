package com.mycompany.soru2;

/**
 *
 * @author burak
 */
public class Soru2 {

    public static void main(String[] args) {
        HillClimbing queens = new HillClimbing();
        System.out.println("| Number of Restarts | Number of Switches | Total Runtime |");
        double[] totalValues = new double[3];
        for(int i=0; i<9;i++){
            double[] values = queens.hillClimbing();
            values[2] /= Math.pow(10,6);
            totalValues[0] += values[0];
            totalValues[1] += values[1];
            totalValues[2] += values[2];
            String restarts = String.format("|%10d%10s", (int)values[0], "|");
            String switches = String.format("%11d%11s", (int)values[1],"|");
            String runtime = String.format("%9.2f ms%4s", Math.round(values[2]*100.0)/100.0,"|");
            System.out.print(restarts);
            System.out.print(switches);
            System.out.println(runtime);
        }
        String avgRestarts = String.format("|%10s%.2f%6s", "Avg:",Math.round(totalValues[0]/15*100.0)/100.0,"|");
        String avgSwitches = String.format("%10s%.2f%7s", "Avg:",Math.round(totalValues[1]/15*100.0)/100.0,"|");
        String avgRuntime = String.format("%6s%.2f ms%3s", "Avg:",Math.round(totalValues[2]/15*100.0)/100.0,"|");
        System.out.print(avgRestarts);
        System.out.print(avgSwitches);
        System.out.println(avgRuntime);
    }
}
