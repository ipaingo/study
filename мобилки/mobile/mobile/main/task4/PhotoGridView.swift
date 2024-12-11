//
//  PhotoGridView.swift
//  sem7project


import SwiftUI

struct PhotoGridView: View {
    var body: some View {
        VStack {
            VStack {
                //
            }
            .frame(width: 200.0, height: 200.0)
            .background(Color(red: 0.9, green: 0.9, blue: 0.9))
            
            Text("Name")
                .multilineTextAlignment(.leading)
        }
    }
}

struct PhotoGridView_Previews: PreviewProvider {
    static var previews: some View {
        PhotoGridView()
    }
}
