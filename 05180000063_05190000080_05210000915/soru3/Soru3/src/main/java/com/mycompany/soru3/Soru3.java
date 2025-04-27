package com.mycompany.soru3;
/**
 *
 * @author burak
 */
import java.util.Arrays;
import java.util.Locale;
import java.util.Random;

public class Soru3 {

    public static char get_random_char(){
        int leftLimit = 32; // "space"
        int rightLimit = 122; // letter 'z'
        int targetStringLength = 1;
        //System.out.println(i);
        Random random = new Random();

        String generatedString = random.ints(leftLimit, rightLimit + 1)
                .limit(targetStringLength)
                .collect(StringBuilder::new, StringBuilder::appendCodePoint, StringBuilder::append)
                .toString();

        if (random.nextBoolean()){
            return generatedString.toUpperCase().charAt(0);
        }else{
            return generatedString.charAt(0);
        }
    }

    public static char[] get_random_char_arr(int length){
        char[] arr = new char[length];

        for (int i = 0; i < length; i++) {
            arr[i] = get_random_char();
        }
        return arr;
    }

    public static void print_2d_char_arr_with_score(char[][] arr, double[] scores){
        for (int i = 0; i < arr.length; i++) {
            for (int j = 0; j < arr[0].length; j++) {
                System.out.print(arr[i][j]);
            }
            System.out.println(scores[i]);
        }
        System.out.println("------------------------------");
    }

    public static char[] get_copy_element_RS(char[][] generation){
        //rank selection
        //assume that array is revers sorted according to their fitness score
        int totalsum = (generation.length) * (generation.length + 1) / 2;

        Random rnd = new Random();
        int random_number = rnd.nextInt(totalsum);
        int partial_sum = 1;
        for (int i = generation.length-1; i >= 0; i--) {
            partial_sum += i;
            if (partial_sum>=random_number){
                return generation[i];
            }
        }
        return generation[generation.length-1];
    }

    public static char[][] get_new_generation(char[][] parents, int elite_size, int population_size){
        char[][] children = new char[population_size][parents[0].length];

        char[][] reversed_parents = new char[parents.length][parents[0].length];
        for (int i = reversed_parents.length-1; i >= 0; i--) {
            reversed_parents[i] = parents[parents.length-i-1];
        }
        int index = 0;
        for (index = 0; index < elite_size; index++) {
            children[index] = reversed_parents[index];
        }

        for (; index < population_size; index++) {
            char[] parent1 = get_copy_element_RS(parents);
            char[] parent2 = get_copy_element_RS(parents);
            /*while (Arrays.equals(parent1, parent2)){
                parent2 = get_copy_element_RS(parents);
            }*/
            children[index] = breed(parent1,parent2);
        }


        return children;
    }

    private static char[] breed(char[] parent1, char[] parent2) {
        char[] child = new char[parent1.length];

        Random rnd = new Random();
        int a = rnd.nextInt(child.length);
        int b = rnd.nextInt(child.length);
        int start = Math.min(a,b);
        int end = Math.max(a,b);

        for (int i = 0; i < child.length; i++) {
            if(i < start || i>end){
                child[i] = parent1[i];
            }else{
                child[i] = parent2[i];
            }
        }
        return child;
    }

    public static void calc_fit_score(char[][] population, double[] scores, char[] pass) {
        for (int i = 0; i < population.length; i++) {
            double matches = 0;
            for (int j = 0; j < pass.length; j++) {
                if (population[i][j] == pass[j]){
                    matches++;
                }
            }
            scores[i] = ((double) matches / pass.length) * 100;
        }
        quickSort(population,scores,0,population.length-1);
    }

    public static void quickSort(char[][] gen,double[] fit_score,int low, int high) {
        if (low < high)
        {
            int pi = partition(gen,fit_score,low, high);

            quickSort(gen,fit_score,low, pi - 1);
            quickSort(gen,fit_score,pi + 1, high);
        }
    }

    public static int partition(char[][] gen,double[] fit_score,int low, int high) {
        double pivot = fit_score[high];
        int i = (low-1);
        for (int j=low; j<high; j++)
        {

            if (fit_score[j] <= pivot)
            {
                i++;
                double temp = fit_score[i];
                char[] temp2 = gen[i];
                fit_score[i] = fit_score[j];
                gen[i] = gen[j];
                fit_score[j] = temp;
                gen[j] = temp2;
            }
        }

        double temp = fit_score[i+1];
        char[] temp2 = gen[i+1];
        fit_score[i+1] = fit_score[high];
        gen[i+1] = gen[high];
        fit_score[high] = temp;
        gen[high] = temp2;
        return i+1;
    }

    public static void mutation(char[][] child_list){
        Random rnd = new Random();
        for (int i = 0; i < child_list.length; i++) {
            if(rnd.nextInt(10)<1){
                child_list[i][rnd.nextInt(child_list[i].length)] = get_random_char();
            }
        }
    }

    public static void main(String[] args) {
        Random rnd = new Random();
        int population_size = 150;
        int number_of_parents = population_size / 5;
        int number_of_elites = population_size / 50;
        //int generation_count = 10;
        String pass_code = "ChatGPT and GPT-4";
        int pass_length = pass_code.length();

        char[][] prev_gen = new char[population_size][pass_length];

        for (int i = 0; i < population_size; i++) {
            prev_gen[i] = get_random_char_arr(pass_length); //first generation
        }

        char[][] parents = new char[number_of_parents][pass_length];
        double[] scores = new double[population_size];
        int count = 1;

        long startTime = System.currentTimeMillis();
        while (scores[population_size-1] != 100 && count<10000) {
            calc_fit_score(prev_gen,scores,pass_code.toCharArray());
            quickSort(prev_gen,scores,0,prev_gen.length-1);
            //print_2d_char_arr_with_score(prev_gen,scores);
            System.out.println("Best score in generation " + count + ": " + scores[population_size-1]);
            System.out.println(String.valueOf(prev_gen[population_size-1]));
            for (int i = 0; i < number_of_parents; i++) {
                parents[i] = get_copy_element_RS(prev_gen);
            }
            double[] parent_fit = new double[number_of_parents];
            calc_fit_score(parents,parent_fit, pass_code.toCharArray());
            //quickSort(parents,parent_fit,0,parents.length-1);

            char[][] next_gen = get_new_generation(parents,number_of_elites,population_size);
            mutation(next_gen);
            calc_fit_score(next_gen,scores,pass_code.toCharArray());
            //print_2d_char_arr(next_gen,scores);
            for (int i = 0; i < prev_gen.length; i++) {
                prev_gen[i] = Arrays.copyOf(next_gen[i], next_gen[i].length);
            }
            count++;
        }
        long endTime = System.currentTimeMillis();
        System.out.println("--------------");
        if(scores[population_size-1] == 100){
            System.out.println("Result found after " + count + " generation.");
            System.out.println(String.valueOf(prev_gen[population_size-1]));
            System.out.println("That took " + (endTime - startTime) + " milliseconds");
        }else{
            System.out.println("After " + count + " generation result couldn't been found. Best score is: " + scores[population_size-1]);
            System.out.println("That took " + (endTime - startTime) + " milliseconds");
        }

        //print_2d_char_arr(temp);


    }
}
