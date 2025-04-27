package com.mycompany.soru2;

/**
 *
 * @author burak
 */
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class HillClimbing {
    private Node node;

    public HillClimbing(){
        node = new Node();
    }

    public double[] hillClimbing(){
        node.randomNode();
        int numberOfSwitches, numberOfRestarts;
        numberOfRestarts = numberOfSwitches = 0;
        double startTime = System.nanoTime();
        while (node.numberOfPairs() != 0){
            Node[] successors = node.generateSuccessors();
            Node bestSuccessor = selectBestNode(successors);
            if(bestSuccessor.numberOfPairs() < node.numberOfPairs()){
                node = bestSuccessor;
                numberOfSwitches++;
            }
            else{
                node.randomNode();
                numberOfRestarts++;
            }
        }
        double endTime = System.nanoTime();
        double totalTime = endTime - startTime;
        return new double[]{(double)numberOfRestarts,(double)numberOfSwitches,totalTime};
    }

    private Node selectBestNode(Node[] successors){
        List<Node> tempNodes = new ArrayList<>();
        int min = Integer.MAX_VALUE;
        for (Node successor : successors) {
            if (successor.numberOfPairs() < min) {
                if (!tempNodes.isEmpty())
                    tempNodes.clear();
                tempNodes.add(successor);
                min = successor.numberOfPairs();
            } else if (successor.numberOfPairs() == min)
                tempNodes.add(successor);
        }
        Random random = new Random();
        int randomIndex = random.nextInt(tempNodes.size());
        return tempNodes.get(randomIndex);
    }




    private class Node{
        public int[] positions = new int[8];
        public void setPositions(int[] positions){
            this.positions = positions;
        }
        public void randomNode(){
            Random random = new Random();
            int[] tempNode = new int[positions.length];
            for(int i = 0; i < positions.length; i++)
                tempNode[i] = random.nextInt(8);
            positions = tempNode;
        }
        public int numberOfPairs(){
            int total = 0;
            //Horizontal search
            for(int i = 0; i<positions.length; i++){
                for(int j=i+1; j<positions.length;j++){
                    if(positions[i] == positions[j])
                        total++;
                }
            }
            //Diagonal search
            for(int i = 0; i<positions.length;i++){
                for(int j=i+1; j<positions.length;j++){
                    if(Math.abs(i-j) == Math.abs(positions[i]-positions[j]))
                        total++;
                }
            }
            return total;
        }
        public Node[] generateSuccessors(){
            Node[] neighbors = new Node[56];
            int counter = 0;
            for(int i = 0; i<positions.length; i++){
                for(int j= 0; j<positions.length; j++){
                    if(positions[i] == j) continue;
                    int[] newPositions = new int[positions.length];
                    System.arraycopy(positions, 0, newPositions,0, positions.length);

                    newPositions[i] = j;
                    Node tempNode = new Node();
                    tempNode.setPositions(newPositions);
                    neighbors[counter++] = tempNode;

                }
            }

            return neighbors;
        
        }
    }
}
    
